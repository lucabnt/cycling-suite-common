"""Device-local background jobs and automatic exchange scheduling.

``JobRegistry`` (from Fuorigiri ``sync_jobs``) runs one job per archive root in
a daemon thread, so networking never holds a UI request or a runtime lock. The
public status is persisted next to the archive; a ``running`` status found
after a restart is reported as interrupted, never as success. Errors expose a
fixed product message only: no URLs, credentials or exception text.

``AutoSchedule`` (from Ammiraglia ``auto_exchange``) decides when an automatic
exchange is due: periodic interval, earlier run after a local change with a
minimum gap, exponential backoff after failures. Times are monotonic seconds.
"""

import json
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .files import write_json


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def backoff(failures, base, cap, max_exponent):
    """Delay after ``failures`` consecutive failures (``failures`` >= 1)."""
    return min(cap, base * 2 ** min(failures - 1, max_exponent))


class AutoSchedule:
    def __init__(self, *, interval, min_gap, retry_base, retry_cap, max_exponent):
        self.interval = interval
        self.min_gap = min_gap
        self.retry_base = retry_base
        self.retry_cap = retry_cap
        self.max_exponent = max_exponent
        self.ran = None
        self.next = 0.0
        self.failures = 0
        self.modified = None

    def due(self, now, modified=None):
        if now < self.next:
            return False
        if self.ran is None or now - self.ran >= self.interval:
            return True
        return modified != self.modified and now - self.ran >= self.min_gap

    def started(self, now):
        self.ran = now

    def failed(self, now):
        self.failures += 1
        self.next = now + backoff(self.failures, self.retry_base, self.retry_cap, self.max_exponent)

    def succeeded(self, modified=None):
        self.failures = 0
        self.next = 0.0
        self.modified = modified


class ObservedTransport:
    """Wrap an immutable-object transport and report inventory/read/write progress."""

    def __init__(self, base, progress):
        self.base = base
        self.progress = progress

    def __getattr__(self, key):
        return getattr(self.base, key)

    def list(self):
        self.progress('inventory')
        return self.base.list()

    def get(self, name):
        self.progress('receiving')
        result = self.base.get(name)
        self.progress('receiving', reads=1)
        return result

    def put(self, name, body):
        self.progress('publishing')
        result = self.base.put(name, body)
        self.progress('publishing', writes=int(bool(result)))
        return result


class JobRegistry:
    def __init__(self, *, product, failed, interrupted, status_file='sync-job.json', persist_every=0.5):
        self.product = product
        self.failed = failed
        self.interrupted = interrupted
        self.status_file = status_file
        self.persist_every = persist_every
        self._guard = threading.RLock()
        self._jobs = {}

    @staticmethod
    def _key(root):
        return str(Path(root).resolve())

    def status(self, root):
        root = Path(root)
        with self._guard:
            job = self._jobs.get(self._key(root))
            if job:
                result = {k: v for k, v in job.items() if not k.startswith('_')}
                if result['status'] == 'running':
                    result['elapsed_s'] = round(time.monotonic() - job['_start'], 1)
                return result
            try:
                result = json.loads((root / self.status_file).read_text(encoding='utf-8'))
            except (ValueError, OSError):
                return {'status': 'idle'}
            if result.get('status') == 'running':
                result.update(status='interrupted', phase='interrupted', error=self.interrupted)
            return result

    def start(self, root, work, **details):
        """Start ``work(progress)`` unless a job is already running for ``root``."""
        root = Path(root)
        key = self._key(root)
        with self._guard:
            previous = self._jobs.get(key)
            if previous and previous['status'] == 'running':
                return self.status(root)
            job = {
                'id': str(uuid4()),
                'status': 'running',
                'phase': 'preparing',
                'started_at': utc_now(),
                **details,
                'reads': 0,
                'writes': 0,
                'elapsed_s': 0,
                '_start': time.monotonic(),
                '_persist': 0,
                '_done': threading.Event(),
            }
            self._jobs[key] = job

            def persist():
                write_json(root / self.status_file, {k: v for k, v in job.items() if not k.startswith('_')})

            persist()

            def progress(phase, reads=0, writes=0):
                with self._guard:
                    job.update(phase=phase, reads=job['reads'] + reads, writes=job['writes'] + writes)
                    if time.monotonic() - job['_persist'] >= self.persist_every:
                        job['elapsed_s'] = round(time.monotonic() - job['_start'], 1)
                        persist()
                        job['_persist'] = time.monotonic()

            def run():
                try:
                    result = work(progress)
                    with self._guard:
                        job.update(status='completed', phase='completed', result=result)
                except Exception:
                    with self._guard:
                        job.update(status='failed', phase='failed', error=self.failed)
                finally:
                    with self._guard:
                        job.update(finished_at=utc_now(), elapsed_s=round(time.monotonic() - job['_start'], 1))
                        try:
                            persist()
                        finally:
                            job['_done'].set()

            threading.Thread(target=run, name=self.product + '-sync-' + job['id'][:8], daemon=True).start()
            return self.status(root)

    def wait(self, root, timeout=540):
        with self._guard:
            event = self._jobs[self._key(root)]['_done']
        event.wait(timeout)
        return self.status(root)
