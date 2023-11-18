import unittest

from _abstract_syntax_tree import *
from _sheet import Sheet


class TestTokenizer(unittest.TestCase):
    def test_evaluate(self):
        with self.subTest(i=0):
            input_ = [
                ["1", "2"],
                ["3", "=A1 + A2 * B1"],
            ]
            sheet = Sheet(input_)
            expected = [
                [NodeNumber(1), NodeNumber(2)],
                [NodeNumber(3), NodeNumber(7)],
            ]
            sheet.evaluate()
            self.assertEqual(sheet._cells, expected)

        with self.subTest(i=1):
            input_ = [
                ["1", "0"],
                ["=A1/B1", "=A2"],
            ]
            sheet = Sheet(input_)
            expected = [
                [NodeNumber(1), NodeNumber(0)],
                [NodeError(), NodeError()],
            ]
            sheet.evaluate()
            self.assertEqual(sheet._cells, expected)
