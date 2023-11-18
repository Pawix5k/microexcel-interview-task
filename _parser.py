from _abstract_syntax_tree import (
    Node,
    NodeBoolean,
    NodeEmpty,
    NodeError,
    NodeFunction,
    NodeInfix,
    NodeNumber,
    NodePrefix,
    NodeReference,
    NodeString,
)
from _tokenizer import Tokenizer, TokenType

INFIX_OPERATORS = {
    "=",
    "<",
    ">",
    "+",
    "-",
    "*",
    "/",
}

PRECEDENCES = {
    "DEFAULT": 0,
    "=": 1,
    "<": 2,
    ">": 2,
    "+": 3,
    "-": 3,
    "*": 4,
    "/": 4,
    "PREFIX": 5,
}


class Parser:
    def __init__(self, input_: str):
        self._tokenizer = Tokenizer(input_)
        self._peek_token = self._tokenizer.next_token()
        self._cur_token = self._peek_token
        self._peek_token = self._tokenizer.next_token()

    def _next_token(self) -> None:
        self._cur_token = self._peek_token
        self._peek_token = self._tokenizer.next_token()

    def parse_cell(self) -> Node:
        if self._cur_token.type_ == TokenType.EOF:
            return NodeEmpty()
        node = self._parse_expression()
        if self._peek_token.type_ != TokenType.EOF:
            return NodeError()
        return node

    def _parse_expression(self, precedence: int = PRECEDENCES["DEFAULT"]) -> Node:
        if self._cur_token.type_ == TokenType.FUNCTION:
            node = self._parse_function()
        elif self._cur_token.type_ == TokenType.NUMBER:
            val = _to_number(self._cur_token.literal)
            node = NodeNumber(val)
        elif self._cur_token.type_ == TokenType.STRING:
            node = NodeString(self._cur_token.literal)
        elif self._cur_token.type_ == TokenType.BOOLEAN:
            val = _to_bool(self._cur_token.literal)
            node = NodeBoolean(val)
        elif self._cur_token.type_ == TokenType.REFERENCE:
            row, col = _reference_to_cords(self._cur_token.literal)
            node = NodeReference(row, col)
        elif self._cur_token.type_ == TokenType.LEFT_PAREN:
            node = self._parse_parenthesized_expression()
        elif self._cur_token.type_ == TokenType.MINUS:
            operator = self._cur_token.literal
            self._next_token()
            node = NodePrefix(operator, self._parse_expression(PRECEDENCES["PREFIX"]))
        else:
            node = NodeError()
        while (
            self._peek_token.literal in INFIX_OPERATORS
            and precedence < PRECEDENCES[self._peek_token.literal]
        ):
            node = NodeInfix(self._peek_token.literal, node)
            self._next_token()
            self._next_token()
            node.right = self._parse_expression(PRECEDENCES[node.operator])
        return node

    def _parse_function(self) -> Node:
        if self._peek_token.type_ != TokenType.LEFT_PAREN:
            return NodeError()
        node = NodeFunction(self._cur_token.literal)
        self._next_token()
        node.args = self._parse_function_arguments()
        if self._peek_token.type_ != TokenType.RIGHT_PAREN:
            return NodeError()
        self._next_token()
        return node

    def _parse_function_arguments(self) -> list[Node]:
        args: list[Node] = []
        if self._peek_token.type_ == TokenType.RIGHT_PAREN:
            return args
        self._next_token()
        args.append(self._parse_expression(PRECEDENCES["DEFAULT"]))
        while self._peek_token.type_ == TokenType.SEMICOLON:
            self._next_token()
            self._next_token()
            args.append(self._parse_expression(PRECEDENCES["DEFAULT"]))

        if self._peek_token.type_ != TokenType.RIGHT_PAREN:
            return [NodeError()]
        return args

    def _parse_parenthesized_expression(self) -> Node:
        self._next_token()
        node = self._parse_expression(PRECEDENCES["DEFAULT"])
        if self._peek_token.type_ != TokenType.RIGHT_PAREN:
            return NodeError()
        self._next_token()

        return node


def _to_number(s: str) -> int | float:
    if "." in s:
        return float(s)
    return int(s)


def _to_bool(s: str) -> bool:
    return s == "TRUE"


def _reference_to_cords(s: str) -> tuple[int, int]:
    s = s.lower()
    col = 0
    i = 0
    while s[i].isalpha():
        col *= 26
        col += ord(s[i]) - ord("a") + 1
        i += 1
    col -= 1
    row = int(s[i:]) - 1
    return row, col
