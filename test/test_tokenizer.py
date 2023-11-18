import unittest

from _tokenizer import Token, Tokenizer, TokenType


class TestTokenizer(unittest.TestCase):
    def test_next_token(self):
        with self.subTest(i=0):
            input_ = "1 + 2 * 3"
            tokenizer = Tokenizer(input_)
            expected_tokens = (
                Token(TokenType.NUMBER, "1"),
                Token(TokenType.PLUS, "+"),
                Token(TokenType.NUMBER, "2"),
                Token(TokenType.ASTERISK, "*"),
                Token(TokenType.NUMBER, "3"),
                Token(TokenType.EOF),
            )
            for expected_token in expected_tokens:
                self.assertEqual(expected_token, tokenizer.next_token())

        with self.subTest(i=1):
            input_ = 'CONCATENATE("Foo"; "Bar")'
            tokenizer = Tokenizer(input_)
            expected_tokens = (
                Token(TokenType.FUNCTION, "CONCATENATE"),
                Token(TokenType.LEFT_PAREN, "("),
                Token(TokenType.STRING, "Foo"),
                Token(TokenType.SEMICOLON, ";"),
                Token(TokenType.STRING, "Bar"),
                Token(TokenType.RIGHT_PAREN, ")"),
                Token(TokenType.EOF),
            )
            for expected_token in expected_tokens:
                self.assertEqual(expected_token, tokenizer.next_token())

        with self.subTest(i=1):
            input_ = 'IF(A2<B2 * B2; CONCATENATE("Foo"); 5.5/5)'
            tokenizer = Tokenizer(input_)
            expected_tokens = (
                Token(TokenType.FUNCTION, "IF"),
                Token(TokenType.LEFT_PAREN, "("),
                Token(TokenType.REFERENCE, "A2"),
                Token(TokenType.LT, "<"),
                Token(TokenType.REFERENCE, "B2"),
                Token(TokenType.ASTERISK, "*"),
                Token(TokenType.REFERENCE, "B2"),
                Token(TokenType.SEMICOLON, ";"),
                Token(TokenType.FUNCTION, "CONCATENATE"),
                Token(TokenType.LEFT_PAREN, "("),
                Token(TokenType.STRING, "Foo"),
                Token(TokenType.RIGHT_PAREN, ")"),
                Token(TokenType.SEMICOLON, ";"),
                Token(TokenType.NUMBER, "5.5"),
                Token(TokenType.SLASH, "/"),
                Token(TokenType.NUMBER, "5"),
                Token(TokenType.RIGHT_PAREN, ")"),
                Token(TokenType.EOF),
            )
            for expected_token in expected_tokens:
                self.assertEqual(expected_token, tokenizer.next_token())

        with self.subTest(i=2):
            input_ = '"dfdffd'
            tokenizer = Tokenizer(input_)
            expected_tokens = (
                Token(TokenType.ERROR),
                Token(TokenType.EOF),
            )
            for expected_token in expected_tokens:
                self.assertEqual(expected_token, tokenizer.next_token())

        with self.subTest(i=3):
            input_ = "-2*-3.4"
            tokenizer = Tokenizer(input_)
            expected_tokens = (
                Token(TokenType.MINUS, "-"),
                Token(TokenType.NUMBER, "2"),
                Token(TokenType.ASTERISK, "*"),
                Token(TokenType.MINUS, "-"),
                Token(TokenType.NUMBER, "3.4"),
                Token(TokenType.EOF),
            )
            for expected_token in expected_tokens:
                self.assertEqual(expected_token, tokenizer.next_token())
