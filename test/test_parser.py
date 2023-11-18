import unittest

from _abstract_syntax_tree import *
from _parser import Parser


class TestTokenizer(unittest.TestCase):
    def test_parse_cell(self):
        with self.subTest(i=0):
            input_ = "1 + 2 * 3"
            parser = Parser(input_)
            expected_tree = NodeInfix(
                "+", NodeNumber(1), NodeInfix("*", NodeNumber(2), NodeNumber(3))
            )
            self.assertEqual(expected_tree, parser.parse_cell())

        with self.subTest(i=1):
            input_ = 'IF(A2<B2 * B2; CONCATENATE("Foo"); 5/5)'
            parser = Parser(input_)
            expected_tree = NodeFunction(
                "IF",
                [
                    NodeInfix(
                        "<",
                        NodeReference(1, 0),
                        NodeInfix("*", NodeReference(1, 1), NodeReference(1, 1)),
                    ),
                    NodeFunction("CONCATENATE", [NodeString("Foo")]),
                    NodeInfix("/", NodeNumber(5), NodeNumber(5)),
                ],
            )
            self.assertEqual(expected_tree, parser.parse_cell())

        with self.subTest(i=2):
            input_ = "IF()"
            parser = Parser(input_)
            expected_tree = NodeFunction("IF")
            self.assertEqual(expected_tree, parser.parse_cell())

        with self.subTest(i=3):
            input_ = "A11*(((2)))+3"
            parser = Parser(input_)
            expected_tree = NodeInfix(
                "+", NodeInfix("*", NodeReference(10, 0), NodeNumber(2)), NodeNumber(3)
            )
            self.assertEqual(expected_tree, parser.parse_cell())

        with self.subTest(i=4):
            input_ = 'A1 * IF() * CONCATENATE("DDD"; F11)'
            parser = Parser(input_)
            expected_tree = NodeInfix(
                "*",
                NodeInfix("*", NodeReference(0, 0), NodeFunction("IF", [])),
                NodeFunction("CONCATENATE", [NodeString("DDD"), NodeReference(10, 5)]),
            )
            self.assertEqual(expected_tree, parser.parse_cell())

        with self.subTest(i=4):
            input_ = "C9"
            parser = Parser(input_)
            expected_tree = NodeReference(8, 2)
            self.assertEqual(expected_tree, parser.parse_cell())

        with self.subTest(i=6):
            input_ = ""
            parser = Parser(input_)
            expected_tree = NodeEmpty()
            self.assertEqual(expected_tree, parser.parse_cell())

        with self.subTest(i=7):
            input_ = "((((()))))"
            parser = Parser(input_)
            expected_tree = NodeError()
            self.assertEqual(expected_tree, parser.parse_cell())

        with self.subTest(i=8):
            input_ = "TRUE"
            parser = Parser(input_)
            expected_tree = NodeBoolean(True)
            self.assertEqual(expected_tree, parser.parse_cell())

        with self.subTest(i=9):
            input_ = "TRUE + IF("
            parser = Parser(input_)
            expected_tree = NodeInfix("+", NodeBoolean(True), NodeError())
            self.assertEqual(expected_tree, parser.parse_cell())

        with self.subTest(i=10):
            input_ = "-2*-3.4"
            parser = Parser(input_)
            expected_tree = NodeInfix(
                "*", NodePrefix("-", NodeNumber(2)), NodePrefix("-", NodeNumber(3.4))
            )
            self.assertEqual(expected_tree, parser.parse_cell())

        with self.subTest(i=11):
            input_ = 'CONCATENATE("DD";"AA")'
            parser = Parser(input_)
            expected_tree = NodeFunction(
                "CONCATENATE", [NodeString("DD"), NodeString("AA")]
            )
            self.assertEqual(expected_tree, parser.parse_cell())
