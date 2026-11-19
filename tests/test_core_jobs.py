"""Shared job runner and automatic exchange schedule."""

import json
import sys
import threading
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'packages/core/src'))

from cycling_suite.jobs import AutoSchedule, JobRegistry, ObservedTransport, backoff  # noqa: E402


class Schedule(unittest.TestCase):
    def schedule(self):
        return AutoSchedule(interval=300, min_gap=30, retry_base=60, retry_cap=1800, max_exponent=5)

    def test_backoff_is_exponential_and_capped(self):
        self.assertEqual([backoff(n, 60, 1800, 5) for n in range(1, 8)], [60, 120, 240, 480, 960, 1800, 1800])
        self.assertEqual([backoff(n, 30, 900, 5) for n in (1, 5, 6)], [30, 480, 900])

    def test_interval_change_gap_and_failures(self):
        s = self.schedule()
        self.assertTrue(s.due(1000, 'm1'))
        s.started(1000)
        s.succeeded('m1')
        self.assertFalse(s.due(1010, 'm1'))
        self.assertFalse(s.due(1010, 'm2'), 'minimum gap after a local change')
        self.assertTrue(s.due(1040, 'm2'), 'a local change brings the exchange forward')
        self.assertFalse(s.due(1040, 'm1'))
        self.assertTrue(s.due(1300, 'm1'), 'periodic exchange')
        s.started(1300)
        s.failed(1300)
        self.assertEqual((s.failures, s.next), (1, 1360))
        self.assertFalse(s.due(1359, 'm9'))
        self.assertTrue(s.due(1360, 'm9'))
        s.started(1360)
        s.failed(1360)
        self.assertEqual(s.next, 1480)
        s.succeeded('m9')
        self.assertEqual((s.failures, s.next), (0, 0.0))


class Registry(unittest.TestCase):
    def registry(self):
        return JobRegistry(product='Test', failed='Errore generico.', interrupted='Interrotto.')

    def test_single_running_job_progress_and_safe_failure(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            jobs = self.registry()
            release = threading.Event()

            def work(progress):
                progress('receiving', reads=2)
                release.wait(5)
                return {'ok': True}

            first = jobs.start(root, work, full_verification=False)
            self.assertEqual(first['status'], 'running')
            self.assertEqual(jobs.start(root, work)['id'], first['id'], 'no overlapping jobs')
            release.set()
            done = jobs.wait(root, 5)
            self.assertEqual((done['status'], done['reads'], done['result']), ('completed', 2, {'ok': True}))
            self.assertFalse(done['full_verification'])

            def broken(progress):
                raise RuntimeError('https://user:secret@example.invalid')

            jobs.start(root, broken)
            failed = jobs.wait(root, 5)
            self.assertEqual((failed['status'], failed['error']), ('failed', 'Errore generico.'))
            self.assertNotIn('secret', (root / 'sync-job.json').read_text(encoding='utf-8'))

    def test_running_status_after_restart_is_interrupted(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'sync-job.json').write_text(json.dumps({'status': 'running', 'id': 'x'}), encoding='utf-8')
            status = self.registry().status(root)
            self.assertEqual((status['status'], status['error']), ('interrupted', 'Interrotto.'))
            self.assertEqual(self.registry().status(root / 'missing'), {'status': 'idle'})

    def test_observed_transport_counts_reads_and_new_writes(self):
        events = []

        class Base:
            remote = True

            def list(self):
                return ['a']

            def get(self, name):
                return b'x'

            def put(self, name, body):
                return name == 'new'

        t = ObservedTransport(Base(), lambda phase, reads=0, writes=0: events.append((phase, reads, writes)))
        t.list()
        t.get('a')
        t.put('new', b'')
        t.put('old', b'')
        self.assertTrue(t.remote)
        self.assertEqual(sum(e[1] for e in events), 1)
        self.assertEqual(sum(e[2] for e in events), 1)


if __name__ == '__main__':
    unittest.main()
