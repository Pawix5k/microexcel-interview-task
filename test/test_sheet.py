import unittest

from _abstract_syntax_tree import *
from _sheet import Sheet


class TestTokenizer(unittest.TestCase):
    def test_evaluate(self) -> None:
        with self.subTest(i=0):
            input_ = [
                ["1", "2"],
                ["3", "=A1 + A2 * B1"],
            ]
            sheet = Sheet(input_)
            expected = [
                ["1", "2"],
                ["3", "7"],
            ]
            self.assertEqual(sheet.evaluate(), expected)

        with self.subTest(i=1):
            input_ = [
                ["1", "0"],
                ["=A1/B1", "=A2"],
            ]
            sheet = Sheet(input_)
            expected = [
                ["1", "0"],
                ["ERROR", "ERROR"],
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
                ["Hello", "World", "HelloWorld"],
                ["5", "3", "Foo"],
                ["1", "FALSE", "TRUE"],
            ]
            self.assertEqual(sheet.evaluate(), expected)

        with self.subTest(i=3):
            input_ = [
                ["=B1", "=A2"],
                ["=B2", "=IF()"],
            ]
            sheet = Sheet(input_)
            expected = [
                ["ERROR", "ERROR"],
                ["ERROR", "ERROR"],
            ]
            self.assertEqual(sheet.evaluate(), expected)

        with self.subTest(i=4):
            input_ = [
                ["=B1", "=A2"],
                ["=B2", "=NONEXISTENT()"],
            ]
            sheet = Sheet(input_)
            expected = [
                ["ERROR", "ERROR"],
                ["ERROR", "ERROR"],
            ]
            self.assertEqual(sheet.evaluate(), expected)

        with self.subTest(i=5):
            input_ = [["=+A2"]]
            sheet = Sheet(input_)
            expected = [["ERROR"]]
            self.assertEqual(sheet.evaluate(), expected)

        with self.subTest(i=6):
            input_ = [['=CONCATENATE("Bar"; 4; TRUE; "Foo")']]
            sheet = Sheet(input_)
            expected = [["Bar4TRUEFoo"]]
            self.assertEqual(sheet.evaluate(), expected)

        with self.subTest(i=7):
            input_ = [["=DFB345 + 5"]]
            sheet = Sheet(input_)
            expected = [["5"]]
            self.assertEqual(sheet.evaluate(), expected)
