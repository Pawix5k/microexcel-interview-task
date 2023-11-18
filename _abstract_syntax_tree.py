from __future__ import annotations

from abc import ABC, abstractmethod


class ImplementsToString(ABC):
    @abstractmethod
    def to_string(self) -> str:
        raise NotImplementedError


class ImplementsToNumber(ABC):
    @abstractmethod
    def to_number(self) -> int | float:
        raise NotImplementedError


class ImplementsToBoolean(ABC):
    @abstractmethod
    def to_string(self) -> bool:
        raise NotImplementedError


class NodeString(ImplementsToString):
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.value}')"

    def __eq__(self, other):
        if isinstance(other, NodeString):
            return self.value == other.value
        return False

    def to_string(self) -> str:
        return self.value


class NodeNumber(ImplementsToString, ImplementsToNumber, ImplementsToBoolean):
    def __init__(self, value: int | float):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def __eq__(self, other):
        if isinstance(other, NodeNumber):
            return self.value == other.value
        return False

    def to_string(self) -> str:
        return str(self.value)

    def to_number(self) -> int:
        return self.value

    def to_boolean(self) -> bool:
        return self.value == 0


class NodeBoolean(ImplementsToString, ImplementsToNumber, ImplementsToBoolean):
    def __init__(self, value: bool):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def __eq__(self, other):
        if isinstance(other, NodeBoolean):
            return self.value == other.value
        return False

    def to_string(self) -> str:
        return str(self.value)

    def to_number(self) -> int:
        return 1 if self.value else 0

    def to_boolean(self) -> bool:
        return self.value


class NodeReference:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __str__(self) -> str:
        return f"REF({self.row}, {self.col})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.row}, {self.col})"

    def __eq__(self, other):
        if isinstance(other, NodeReference):
            return (self.row, self.col) == (other.row, other.col)
        return False


class NodeFunction:
    def __init__(self, name: str, args: list[Node] = []):
        self.name = name
        self.args = args

    def __str__(self) -> str:
        args_str = "; ".join(str(node) for node in self.args)
        return f"{self.name}({args_str})"

    def __repr__(self) -> str:
        args_repr = ", ".join(repr(arg) for arg in self.args)
        return f"{self.__class__.__name__}('{self.name}', [{args_repr}])"

    def __eq__(self, other):
        if isinstance(other, NodeFunction) and len(self.args) == len(other.args):
            for own_arg, other_arg in zip(self.args, other.args):
                if own_arg != other_arg:
                    return False
            return True
        return False


class NodeEmpty(ImplementsToString, ImplementsToNumber, ImplementsToBoolean):
    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __eq__(self, other):
        return isinstance(other, NodeEmpty)

    def to_string(self) -> str:
        return ""

    def to_number(self) -> int:
        return 0

    def to_boolean(self) -> bool:
        return False


class NodePrefix:
    def __init__(self, operator: str, expression: Node):
        self.operator = operator
        self.expression = expression

    def __str__(self) -> str:
        return f"({self.operator}{str(self.expression)})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.operator}', {repr(self.expression)})"

    def __eq__(self, other):
        if isinstance(other, NodePrefix):
            return (
                self.operator == other.operator and self.expression == other.expression
            )
        return False


class NodeInfix:
    def __init__(self, operator: str, left: Node, right: Node = NodeEmpty()):
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f"({str(self.left)} {self.operator} {str(self.right)})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.operator}', {repr(self.left)}, {repr(self.right)})"

    def __eq__(self, other):
        if isinstance(other, NodeInfix):
            return (
                self.operator == other.operator
                and self.left == other.left
                and self.right == other.right
            )
        return False


class NodeError:
    def __str__(self) -> str:
        return "ERROR"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __eq__(self, other):
        return isinstance(other, NodeError)


Node = (
    NodeString
    | NodeNumber
    | NodeBoolean
    | NodeReference
    | NodeFunction
    | NodePrefix
    | NodeInfix
    | NodeEmpty
    | NodeError
)
