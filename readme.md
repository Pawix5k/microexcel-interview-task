# MicroExcel

## Task description

Implement a program that simulates MS Excel.
The script must accept and output headerless `.csv` file.

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