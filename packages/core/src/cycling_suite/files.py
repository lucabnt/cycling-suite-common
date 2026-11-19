"""Atomic local writes: no partial file is ever visible under the final name.

The temporary file sits in the destination directory, is flushed to disk and
restricted to the owner before ``os.replace``. Derived from Ammiraglia
``vault.atomic`` and Fuorigiri ``write_json``.
"""

import os
import tempfile
from pathlib import Path

from .canonical import canonical


def atomic_write(path, raw, *, mode=0o600):
    path = Path(path)
    fd, name = tempfile.mkstemp(dir=path.parent, suffix='.pending')
    temp = Path(name)
    try:
        with os.fdopen(fd, 'wb') as out:
            out.write(raw)
            out.flush()
            os.fsync(out.fileno())
        os.chmod(temp, mode)
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def write_json(path, value, *, mode=0o600):
    atomic_write(path, canonical(value).encode('utf-8'), mode=mode)
