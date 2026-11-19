"""Exchange invariants shared by the app sync engines."""

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'packages/core/src'))

from cycling_suite.exchange import add_version, event_names, incremental, publish_immutable  # noqa: E402
from cycling_suite.transports import FolderTransport  # noqa: E402


class Fork(Exception):
    pass


class Exchange(unittest.TestCase):
    def test_same_version_with_different_content_is_a_fork(self):
        versions = {}
        add_version(versions, 1, {'members': ['a'], 'version': 1}, Fork)
        add_version(versions, 1, {'version': 1, 'members': ['a']}, Fork)
        add_version(versions, 2, {'members': ['a', 'b'], 'version': 2}, Fork)
        self.assertEqual(sorted(versions), [1, 2])
        with self.assertRaises(Fork):
            add_version(versions, 1, {'members': ['b'], 'version': 1}, Fork)
        with self.assertRaises(Fork):
            add_version(versions, 2, {'members': ['a', 'b'], 'version': 2.0}, Fork)

    def test_incremental_skips_known_ids_unless_full_verification(self):
        names = ['b.ev', 'a.ev', 'c.ev', 'other.json', '.ev']
        self.assertEqual(event_names(names, '.ev'), {'a': 'a.ev', 'b': 'b.ev', 'c': 'c.ev'})
        self.assertEqual(incremental(names, '.ev', {'b'}, False), ([('a', 'a.ev'), ('c', 'c.ev')], 1))
        self.assertEqual(incremental(names, '.ev', {'b'}, True)[1], 0)
        self.assertEqual([n for _, n in incremental(names, '.ev', {'b'}, True)[0]], ['a.ev', 'b.ev', 'c.ev'])

    def test_collision_accepted_only_when_the_app_confirms_the_same_content(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'x').mkdir()
            transport = FolderTransport(root / 'x', 'channel', root / 'data', prefix='test')
            self.assertTrue(publish_immutable(transport, 'e.ev', b'cipher-1', lambda raw: False))
            self.assertFalse(publish_immutable(transport, 'e.ev', b'cipher-1', lambda raw: False))
            self.assertFalse(publish_immutable(transport, 'e.ev', b'cipher-2', lambda raw: raw == b'cipher-1'))
            with self.assertRaises(ValueError):
                publish_immutable(transport, 'e.ev', b'cipher-3', lambda raw: False)
            self.assertEqual(transport.get('e.ev'), b'cipher-1')


if __name__ == '__main__':
    unittest.main()
