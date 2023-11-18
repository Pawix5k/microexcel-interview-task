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
            self.assertEqual(sheet.evaluate(), expected)

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
            self.assertEqual(sheet.evaluate(), expected)

        with self.subTest(i=2):
            input_ = [
                ["Hello", "World", "=CONCATENATE(A1;B1)"],
                ["5", "3", '=IF(A2<B2 * B2; CONCATENATE("Foo"); 5/5)'],
                ["1", "=A3=A2", "=A3<A2"],
            ]
            sheet = Sheet(input_)
            expected = [
                [
                    NodeString("Hello"),
                    NodeString("World"),
                    NodeString("HelloWorld"),
                ],
                [NodeNumber(5), NodeNumber(3), NodeString("Foo")],
                [NodeNumber(1), NodeBoolean(False), NodeBoolean(True)],
            ]
            self.assertEqual(sheet.evaluate(), expected)
