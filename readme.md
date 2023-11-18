# MicroExcel

## Task description

Implement a program that simulates MS Excel.
The script must accept and output headerless `.csv` file.

Program should be written in Python and use no external libraries.

The program must be able to perform basic arithmetic operations (addition, subtraction, multiplication, division) and comparison operations (less than, larger than, equals) in formulas and evaluate them in correct order.

The program should be able to handle string, number and boolean primitives.

The program must also implement functions [IF](https://support.microsoft.com/en-us/office/if-function-69aed7c9-4e8a-4755-a9bc-aa8bbff73be2) and [CONCATENATE](https://support.microsoft.com/en-us/office/concatenate-function-8f8ae884-2ca8-4f7a-b093-75d702bea31d) functions in which arguments are delimited by semicolon `;`.

The program must handle and propagate errors like zero division, circular reference or bad arguments to functions.

Columns are labeled `A, B, C, ..., AA, AB...` from left to right. Rows are labeled numerically and 1-indexed from top to bottom. `C2` indicates a cell in the the third column and the second row.

Cells with formulas start with `=` character.

### Examples:
input:
```csv
1,2
3,=A1 + A2 * B1
```
output:
```csv
1,2
3,7
```
___

input:
```csv
1,0
=A1/B1,=A2
```
output:
```csv
1,0
ERROR,ERROR
```
___
input:
```csv
Hello,World,=CONCATENATE(A1;B1)
5,3,=IF(A2<B2 * B2; CONCATENATE("Foo"); 5/5)
1,=A3=A2,=A3<A2
```
output:
```csv
Hello,World,HelloWorld
5,3,Foo
1,FALSE,TRUE
```

## Solution

My program takes following steps when evaluating final state of input sheet.

### I. tokenization

In case of string, number or boolean initial values the actual parsing step involving tokenization is skipped. In case of formulas (cells starting with `=`) `Tokenizer` divides the input into individual tokens. Possible token type values:
```
EOF
EQUALS
PLUS
MINUS
ASTERISK
SLASH
LT
GT
EQ
SEMICOLON
LEFT_PAREN
RIGHT_PAREN
STRING
NUMBER
BOOLEAN
REFERENCE
ERROR
FUNCTION
```
Most of them also includes string literal.

### II. Parsing

Next step is assembling an Abstract Syntax Tree from tokens. My `Parses` uses recursive descent to create individual Nodes and build an AST in correct order of operations.

Nodes themselves (in `_abstract_syntax_tree.py` module) are made up from multiple different classes, all of them implementing `__str__` and `__eq__` dunder methods for easier stringification and testing for equality.

All the classes making up Node:
```
NodeString
NodeNumber
NodeBoolean
NodeReference
NodeFunction
NodePrefix
NodeInfix
NodeEmpty
NodeError
```

### III. Evaluation

Parsed sheet is 2D list of leafs/trees made up of nodes. Because of possible references, the structure is a graph.

Given that fact, when evaluating individual nodes, depth first search is done. Track of visited cells is kept for cycle detection and resolving it as an error.

When reference is evaluated, result is saved directly to the corrresponding cell in `Sheet` to avoid computing the same tree multiple times.


## Usage

### Running the program

From root folder:
```
python main.py <input_path> <output_path>
```
or
```
python3 main.py <input_path> <output_path>
```
for example:
```
python main.py example_input\input3.csv out.csv
```

### Running test

From root folder:
```
python -m unittest
```
or
```
python3 -m unittest
```
