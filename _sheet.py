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

SETTLED_NODES = (
    NodeBoolean,
    NodeEmpty,
    NodeError,
    NodeNumber,
    NodeString,
)


def prefix_sub_handler(node: Node):
    if isinstance(node, ImplementsToNumber):
        return NodeNumber(-node.to_number())
    return NodeError()


PREFIX_HANDLERS = {
    "-": prefix_sub_handler,
}


def add_handler(left, right):
    if isinstance(left, ImplementsToNumber) and isinstance(right, ImplementsToNumber):
        return NodeNumber(left.to_number() + right.to_number())
    return NodeError()


def sub_handler(left, right):
    if isinstance(left, ImplementsToNumber) and isinstance(right, ImplementsToNumber):
        return NodeNumber(left.to_number() - right.to_number())
    return NodeError()


def mul_handler(left, right):
    if isinstance(left, ImplementsToNumber) and isinstance(right, ImplementsToNumber):
        return NodeNumber(left.to_number() * right.to_number())
    return NodeError()


def div_handler(left, right):
    if isinstance(left, ImplementsToNumber) and isinstance(right, ImplementsToNumber):
        if right.to_number() == 0:
            return NodeError()
        return NodeNumber(left.to_number() * right.to_number())
    return NodeError()


def div_handler(left, right):
    if isinstance(left, ImplementsToNumber) and isinstance(right, ImplementsToNumber):
        if right.to_number() == 0:
            return NodeError()
        return NodeNumber(left.to_number() * right.to_number())
    return NodeError()


def lt_handler(left, right):
    if isinstance(left, ImplementsToNumber) and isinstance(right, ImplementsToNumber):
        if left.to_number() < right.to_number():
            return NodeBoolean(True)
        return NodeBoolean(False)
    return NodeError()


def gt_handler(left, right):
    if isinstance(left, ImplementsToNumber) and isinstance(right, ImplementsToNumber):
        if left.to_number() > right.to_number():
            return NodeBoolean(True)
        return NodeBoolean(False)
    return NodeError()


def eq_handler(left, right):
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


def fn_concatenate_handler(args):
    strs = []
    for arg in args:
        if not isinstance(arg, ImplementsToString):
            return NodeError()
        strs.append(arg.to_string())
    return NodeString("".join(strs))


def fn_if_handler(args):
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

    def _load(self, raw_cells):
        cells = []
        for row in raw_cells:
            nodes_row = []
            for cell in row:
                nodes_row.append(self._parse_cell(cell))
            cells.append(nodes_row)
        return cells

    def _parse_cell(self, cell: str):
        if cell.startswith("="):
            node = Parser(cell[1:]).parse_cell()
            return node
        try:
            return NodeNumber(int(cell))
        except ValueError:
            try:
                return NodeNumber(float(cell))
            except ValueError:
                return NodeString(cell)

    def evaluate(self):
        for row in range(len(self._cells)):
            for col in range(len(self._cells[row])):
                self._evaluate_cell(row, col)
        return self._cells

    def _evaluate_cell(self, row, col, visited=set()):
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

    def _in_sheet(self, row, col):
        if 0 <= row < len(self._cells) and 0 <= col < len(self._cells[row]):
            return True
        return False

    def _evaluate_node(self, node, visited=set()):
        if isinstance(node, SETTLED_NODES):
            return node
        if isinstance(node, NodeReference):
            return self._evaluate_cell(node.row, node.col, visited)
        if isinstance(node, NodePrefix):
            return PREFIX_HANDLERS[node.operator](
                self._evaluate_node(node.expression, visited)
            )
        if isinstance(node, NodeInfix):
            return INFIX_HANDLERS[node.operator](
                self._evaluate_node(node.left, visited),
                self._evaluate_node(node.right, visited),
            )
        if isinstance(node, NodeFunction):
            return FUNCTION_HANDLERS[node.name](
                [self._evaluate_node(arg, visited) for arg in node.args]
            )
