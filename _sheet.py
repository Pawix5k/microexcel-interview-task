from _abstract_syntax_tree import (
    ImplementsToBoolean,
    ImplementsToNumber,
    ImplementsToString,
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
from _parser import Parser

Cells = list[list[Node]]

SETTLED_NODES = (
    NodeBoolean,
    NodeEmpty,
    NodeError,
    NodeNumber,
    NodeString,
)


def prefix_sub_handler(node: Node) -> NodeNumber | NodeError:
    if isinstance(node, ImplementsToNumber):
        return NodeNumber(-node.to_number())
    return NodeError()


PREFIX_HANDLERS = {
    "-": prefix_sub_handler,
}


def add_handler(left: Node, right: Node) -> NodeNumber | NodeError:
    if isinstance(left, ImplementsToNumber) and isinstance(right, ImplementsToNumber):
        return NodeNumber(left.to_number() + right.to_number())
    return NodeError()


def sub_handler(left: Node, right: Node) -> NodeNumber | NodeError:
    if isinstance(left, ImplementsToNumber) and isinstance(right, ImplementsToNumber):
        return NodeNumber(left.to_number() - right.to_number())
    return NodeError()


def mul_handler(left: Node, right: Node) -> NodeNumber | NodeError:
    if isinstance(left, ImplementsToNumber) and isinstance(right, ImplementsToNumber):
        return NodeNumber(left.to_number() * right.to_number())
    return NodeError()


def div_handler(left: Node, right: Node) -> NodeNumber | NodeError:
    if isinstance(left, ImplementsToNumber) and isinstance(right, ImplementsToNumber):
        if right.to_number() == 0:
            return NodeError()
        return NodeNumber(left.to_number() * right.to_number())
    return NodeError()


def lt_handler(left: Node, right: Node) -> NodeBoolean | NodeError:
    if isinstance(left, ImplementsToNumber) and isinstance(right, ImplementsToNumber):
        if left.to_number() < right.to_number():
            return NodeBoolean(True)
        return NodeBoolean(False)
    return NodeError()


def gt_handler(left: Node, right: Node) -> NodeBoolean | NodeError:
    if isinstance(left, ImplementsToNumber) and isinstance(right, ImplementsToNumber):
        if left.to_number() > right.to_number():
            return NodeBoolean(True)
        return NodeBoolean(False)
    return NodeError()


def eq_handler(left: Node, right: Node) -> NodeBoolean | NodeError:
    return NodeBoolean(left == right)


INFIX_HANDLERS = {
    "+": add_handler,
    "-": sub_handler,
    "*": mul_handler,
    "/": div_handler,
    "<": lt_handler,
    ">": gt_handler,
    "=": eq_handler,
}


def fn_concatenate_handler(args: list[Node]) -> NodeString | NodeError:
    strs = []
    for arg in args:
        if not isinstance(arg, ImplementsToString):
            return NodeError()
        strs.append(arg.to_string())
    return NodeString("".join(strs))


def fn_if_handler(args: list[Node]) -> Node:
    if len(args) == 3 and isinstance(args[0], ImplementsToBoolean):
        if args[0].to_boolean():
            return args[1]
        return args[2]
    return NodeError()


FUNCTION_HANDLERS = {
    "CONCATENATE": fn_concatenate_handler,
    "IF": fn_if_handler,
}


class Sheet:
    def __init__(self, raw_cells: list[list[str]]):
        self._cells = self._load(raw_cells)

    def _load(self, raw_cells: list[list[str]]) -> Cells:
        cells = []
        for row in raw_cells:
            nodes_row = []
            for cell in row:
                nodes_row.append(self._parse_cell(cell))
            cells.append(nodes_row)
        return cells

    def _parse_cell(self, cell: str) -> Node:
        if cell.startswith("="):
            node = Parser(cell[1:]).parse_formula()
            return node
        try:
            return NodeNumber(int(cell))
        except ValueError:
            try:
                return NodeNumber(float(cell))
            except ValueError:
                return NodeString(cell)

    def evaluate(self) -> list[list[str]]:
        for row in range(len(self._cells)):
            for col in range(len(self._cells[row])):
                self._evaluate_cell(row, col)
        return self._stringified()

    def _stringified(self) -> list[list[str]]:
        return [[str(cell) for cell in row] for row in self._cells]

    def _evaluate_cell(
        self, row: int, col: int, visited: set[tuple[int, int]] = set()
    ) -> Node:
        if not self._in_sheet(row, col):
            return NodeEmpty()
        if ((row, col)) in visited:
            return NodeError()
        node = self._cells[row][col]
        visited.add((row, col))
        node = self._evaluate_node(node, visited)
        self._cells[row][col] = node
        visited.remove((row, col))
        return node

    def _in_sheet(self, row: int, col: int) -> bool:
        if 0 <= row < len(self._cells) and 0 <= col < len(self._cells[row]):
            return True
        return False

    def _evaluate_node(self, node: Node, visited: set[tuple[int, int]] = set()) -> Node:
        if isinstance(node, SETTLED_NODES):
            return node
        if isinstance(node, NodeReference):
            return self._evaluate_cell(node.row, node.col, visited)
        if isinstance(node, NodePrefix):
            if node.operator in PREFIX_HANDLERS:
                return PREFIX_HANDLERS[node.operator](
                    self._evaluate_node(node.expression, visited)
                )
            return NodeError
        if isinstance(node, NodeInfix):
            if node.operator in INFIX_HANDLERS:
                return INFIX_HANDLERS[node.operator](
                    self._evaluate_node(node.left, visited),
                    self._evaluate_node(node.right, visited),
                )
            return NodeError()
        if isinstance(node, NodeFunction):
            if node.name in FUNCTION_HANDLERS:
                return FUNCTION_HANDLERS[node.name](
                    [self._evaluate_node(arg, visited) for arg in node.args]
                )
            return NodeError()
