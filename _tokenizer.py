from __future__ import annotations

import re
from enum import Enum, auto
from typing import Any

REFERENCE_PATTERN = re.compile(r"[a-zA-Z]+[0-9]+")


class TokenType(Enum):
    EOF = auto()
    EQUALS = auto()
    PLUS = auto()
    MINUS = auto()
    ASTERISK = auto()
    SLASH = auto()
    LT = auto()
    GT = auto()
    EQ = auto()
    SEMICOLON = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    REFERENCE = auto()
    ERROR = auto()
    FUNCTION = auto()


class Token:
    def __init__(self, type_: TokenType, literal: str = "") -> None:
        self.type_ = type_
        self.literal = literal

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Token):
            if self.type_ == other.type_ and self.literal == other.literal:
                return True
        return False

    def __repr__(self) -> str:
        return f'Token({self.type_}, "{self.literal}")'


class Tokenizer:
    def __init__(self, input: str) -> None:
        self._input = input
        self._cur_pos = 0
        self._ch = ""
        self._next_char()

    def _next_char(self) -> None:
        if self._cur_pos < len(self._input):
            self._ch = self._input[self._cur_pos]
            self._cur_pos += 1
        else:
            self._ch = "\0"

    def _peek_char(self) -> str:
        if self._cur_pos < len(self._input):
            return self._input[self._cur_pos]
        return "\0"

    def next_token(self) -> Token:
        while self._ch.isspace() and self._ch != "\0":
            self._next_char()

        token = Token(TokenType.ERROR)

        if self._ch == "\0":
            token = Token(TokenType.EOF)
        elif self._ch == "+":
            token = Token(TokenType.PLUS, "+")
        elif self._ch == "-":
            token = Token(TokenType.MINUS, "-")
        elif self._ch == "*":
            token = Token(TokenType.ASTERISK, "*")
        elif self._ch == "/":
            token = Token(TokenType.SLASH, "/")
        elif self._ch == "=":
            token = Token(TokenType.EQUALS, "=")
        elif self._ch == "<":
            token = Token(TokenType.LT, "<")
        elif self._ch == ">":
            token = Token(TokenType.GT, ">")
        elif self._ch == "(":
            token = Token(TokenType.LEFT_PAREN, "(")
        elif self._ch == ")":
            token = Token(TokenType.RIGHT_PAREN, ")")
        elif self._ch == ";":
            token = Token(TokenType.SEMICOLON, ";")
        elif self._ch == '"':
            chars = []
            while self._peek_char() not in ('"', "\0"):
                self._next_char()
                chars.append(self._ch)
            if self._peek_char() == '"':
                token = Token(TokenType.STRING, "".join(chars))
                self._next_char()
        elif self._ch.isalnum():
            chars = []
            chars.append(self._ch)
            while self._peek_char().isalnum() or self._peek_char() == ".":
                self._next_char()
                chars.append(self._ch)
            literal: str = "".join(chars)

            if self._peek_char() == "(":
                token = Token(TokenType.FUNCTION, literal)
            elif literal in ("TRUE", "FALSE"):
                token = Token(TokenType.BOOLEAN, literal)
            elif _is_number(literal):
                token = Token(TokenType.NUMBER, literal)
            elif _is_reference(literal):
                token = Token(TokenType.REFERENCE, literal)

        self._next_char()

        return token


def _is_reference(s: str) -> bool:
    if REFERENCE_PATTERN.fullmatch(s):
        return True
    return False


def _is_number(s: str) -> bool:
    try:
        float(s)
    except ValueError:
        return False
    return True
