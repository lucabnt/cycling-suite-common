"""Spreadsheet formula neutralization for exported CSV text cells.

A text cell is prefixed with an apostrophe when it starts with tab, CR or LF,
or when its first non-blank character is = + - @, so a spreadsheet shows it as
text instead of evaluating it. Text that reads as a number (``-12.5``,
``-12,5``, `` -3``) is left untouched. The mapping is reversible with
``restore``, also for text that originally started with an apostrophe.

Union of Fuorigiri RT-15 (numbers intact, reversible) and Ammiraglia
``exports.safe_cell`` (leading blanks and line breaks hiding a formula).
"""

import csv

FORMULA = ('=', '+', '-', '@')
CONTROL = ('\t', '\r', '\n')


def _numeric(text):
    try:
        float(text.replace(',', '.'))
        return True
    except ValueError:
        return False


def needs_prefix(text):
    if not text:
        return False
    if text[0] == "'":
        return needs_prefix(text[1:])
    risky = text[0] in CONTROL or text.lstrip()[:1] in FORMULA
    return risky and not _numeric(text)


def neutralize(value):
    return "'" + value if isinstance(value, str) and needs_prefix(value) else value


def restore(value):
    if isinstance(value, str) and value.startswith("'") and needs_prefix(value[1:]):
        return value[1:]
    return value


class DictWriter(csv.DictWriter):
    def writerow(self, rowdict):
        return super().writerow({k: neutralize(v) for k, v in rowdict.items()})

    def writerows(self, rowdicts):
        return super().writerows({k: neutralize(v) for k, v in row.items()} for row in rowdicts)


class writer:
    def __init__(self, stream, **options):
        self._writer = csv.writer(stream, **options)

    def writerow(self, row):
        return self._writer.writerow([neutralize(v) for v in row])

    def writerows(self, rows):
        return self._writer.writerows([neutralize(v) for v in row] for row in rows)
