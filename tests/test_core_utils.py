"""Shared utilities: CSV formula neutralization, atomic writes, fixed attribution."""

import csv
import io
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'packages/core/src'))

from cycling_suite import csv_safety, files  # noqa: E402
from cycling_suite.branding import ATTRIBUTION  # noqa: E402
from cycling_suite.canonical import canonical  # noqa: E402


class CsvSafety(unittest.TestCase):
    def test_formulas_hidden_by_blanks_or_breaks_are_neutralized(self):
        for text in ('=1+1', '+A1', '-cmd', '@SUM(A1)', ' =1+1', ' =x', '\t=x', '\rabc', '\nabc', '\tabc'):
            self.assertEqual(csv_safety.neutralize(text), "'" + text, repr(text))

    def test_numbers_and_plain_text_are_untouched(self):
        for value in ('-12.5', '-12,5', ' -3', '+4', 'testo', '', 'a=b', 12, -3.5, None, True):
            self.assertEqual(csv_safety.neutralize(value), value, repr(value))

    def test_mapping_is_reversible_also_for_leading_apostrophes(self):
        for text in ('=x', "'=x", "''=x", "'testo", 'testo', '-12', ' =x', '\nabc'):
            self.assertEqual(csv_safety.restore(csv_safety.neutralize(text)), text, repr(text))

    def test_writers_neutralize_every_cell(self):
        out = io.StringIO()
        writer = csv_safety.DictWriter(out, fieldnames=['a', 'b'])
        writer.writerows([{'a': '=1', 'b': '-2'}])
        csv_safety.writer(out).writerow(['@x', 3])
        rows = list(csv.reader(io.StringIO(out.getvalue())))
        self.assertEqual(rows, [["'=1", '-2'], ["'@x", '3']])


class Files(unittest.TestCase):
    def test_atomic_json_replaces_without_leftovers(self):
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / 'state.json'
            files.write_json(path, {'b': 1, 'a': 'è'})
            files.write_json(path, {'b': 2})
            self.assertEqual(path.read_text(encoding='utf-8'), canonical({'b': 2}))
            self.assertEqual(json.loads(path.read_text(encoding='utf-8')), {'b': 2})
            self.assertEqual([p.name for p in Path(temporary).iterdir()], ['state.json'])

    def test_failed_write_keeps_previous_content(self):
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / 'state.json'
            files.write_json(path, {'ok': True})
            with self.assertRaises(ValueError):
                files.write_json(path, {'bad': float('nan')})
            self.assertEqual(json.loads(path.read_text(encoding='utf-8')), {'ok': True})


class Branding(unittest.TestCase):
    def test_attribution_is_the_fixed_text(self):
        self.assertEqual(ATTRIBUTION, 'Sviluppato da Luca Bontempi per Progetto Ciclismo - Rodengo Saiano A.S.D.')


if __name__ == '__main__':
    unittest.main()
