"""Byte-for-byte compatibility of cycling_suite.crypto with the app formats.

The vectors in tests/vectors were produced by the Fuorigiri and Ammiraglia
implementations before extraction (same deterministic randomness and clock).
Requires ``cryptography``: run with an app virtual environment when the
global interpreter does not provide it.
"""

import base64
import itertools
import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'packages/core/src'))
VECTORS = ROOT / 'tests/vectors'

try:
    import cryptography  # noqa: F401
except ImportError:  # pragma: no cover - reported as skip
    if os.environ.get('CYCLING_SUITE_REQUIRE_CRYPTO') == '1':
        raise
    cryptography = None

FIXED_TIME = 1795000000
PASSWORD = 'password-di-prova-12'


def stream(seed):
    counter = itertools.count()

    def urandom(n):
        return bytes((seed + next(counter) * 7 + i) % 256 for i in range(n))

    return urandom


def vectors(name):
    return json.loads((VECTORS / f'crypto-{name}.json').read_text(encoding='utf-8'))


@unittest.skipIf(cryptography is None, 'cryptography non installato: usare la venv di un consumatore')
class CryptoVectors(unittest.TestCase):
    def setUp(self):
        from cycling_suite import crypto

        self.c = crypto

    def test_canonical_and_signatures_match_both_apps(self):
        for name in ('fuorigiri', 'ammiraglia'):
            v = vectors(name)
            self.assertEqual(self.c.canonical(v['value']), v['canonical'])
        f = vectors('fuorigiri')
        self.assertEqual(self.c.sign_value(f['ed25519_private'], f['value']), f['ed25519_signature'])
        a = vectors('ammiraglia')
        self.assertEqual(self.c.public_key(a['ed25519_private']), a['public'])
        self.assertEqual(self.c.sign_value(a['ed25519_private'], a['value']), a['envelope']['signature'])
        self.assertEqual(self.c.digest(a['value']), a['hashed'])
        self.c.verify_value(a['public'], a['value'], a['envelope']['signature'])
        from cryptography.exceptions import InvalidSignature

        with self.assertRaises(InvalidSignature):
            self.c.verify_value(a['public'], {**a['value'], 'z': 1}, a['envelope']['signature'])
        self.assertEqual(
            self.c.derived_seed(
                a['ed25519_private'], 'ammiraglia-renewal-key-v1', 'canale', '00000000-0000-4000-8000-000000000001'
            ),
            a['renewal_key'],
        )

    def test_fuorigiri_json_envelope_is_identical_and_reads_legacy(self):
        v = vectors('fuorigiri')
        with (
            mock.patch('cycling_suite.crypto.os.urandom', stream(11)),
            mock.patch('cryptography.fernet.os.urandom', stream(91)),
            mock.patch('cryptography.fernet.time.time', lambda: FIXED_TIME),
        ):
            raw = self.c.seal_json(v['value'], PASSWORD, self.c.ScryptParams(2**17))
        self.assertEqual(raw.decode(), v['seal_json'])
        legacy = self.c.ScryptParams(2**14)
        for envelope in (v['seal_json'], v['seal_json_legacy']):
            self.assertEqual(self.c.unseal_json(envelope.encode(), PASSWORD, legacy=legacy, unsupported='x'), v['value'])
        crafted = json.loads(v['seal_json'])
        for kdf in ({'name': 'scrypt', 'n': 2**21, 'r': 8, 'p': 1}, {'name': 'scrypt', 'n': 3 * 2**14, 'r': 8, 'p': 1}):
            with self.assertRaisesRegex(ValueError, 'non supportati'):
                self.c.unseal_json(
                    json.dumps({**crafted, 'kdf': kdf}).encode(), PASSWORD, legacy=legacy, unsupported='non supportati'
                )

    def test_ammiraglia_aead_frames_are_identical(self):
        import struct

        v = vectors('ammiraglia')
        raw = self.c.canonical(v['value']).encode()
        params = self.c.ScryptParams(2**17)
        with mock.patch('cycling_suite.crypto.os.urandom', stream(23)):
            salt = self.c.os.urandom(16)
            prefix = b'AMMBA002' + struct.pack('>III', params.n, params.r, params.p) + salt
            sealed = self.c.aead_seal(raw, self.c.derive_key('passphrase-di-prova', salt, params), prefix)
        self.assertEqual(base64.b64encode(sealed).decode(), v['vault_seal'])
        self.assertEqual(
            self.c.aead_open(sealed, self.c.derive_key('passphrase-di-prova', salt, params), len(prefix) + 12), raw
        )
        secret = bytes(range(32, 64))
        with mock.patch('cycling_suite.crypto.os.urandom', stream(31)):
            framed = self.c.aead_seal(raw, secret, b'AMMDB002' + bytes(16))
        self.assertEqual(base64.b64encode(framed).decode(), v['vault_encrypt'])
        from cryptography.exceptions import InvalidTag

        with self.assertRaises(InvalidTag):
            self.c.aead_open(framed[:-1] + bytes([framed[-1] ^ 1]), secret, 36)


if __name__ == '__main__':
    unittest.main()
