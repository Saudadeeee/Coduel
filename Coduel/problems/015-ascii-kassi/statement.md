![/problems/asciikassi/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/asciikassi/file/statement/en/img-0001.jpg)
Photo from the collection of the High School Programmin
Contest of Iceland

Today the High School Programming Contest of Iceland is
hosted on Kattis, which reviews the solutions from contestants
upon their submission. Most of the process has been automated,
but it wasn’t always this way.

Some years ago, judges walked from contestant to contestant,
to check whether the outputs from each team were correct. This
was done by asking contestants to put a piece of paper on their
monitor so the judges could see the contestant thought they had
solved a task. The judge then asked the contestant to start up
the program and enter a specific input which the judge had
carefully selected and then the judge verified the
correctness.

The head judge in these days, Algrímur, requires your
assistance with judging a particular task. Algrímur usually
writes his own solutions for the tasks and then prints on a
paper a few outputs for specific inputs. But Algrímur has been
too busy to write his own solution.

The task at hand involves drawing a square in the output,
using only the symbols | , - , + and spaces.

The left and right sides of the square should be drawn using
the symbol | , while the top and
bottom sides of the should be drawn using the symbol - . Corners should be drawn using the symbol + and the interior of the square
should be made up of spaces.

Can you write a solution for Algrímur so he can print the
output on paper?

## Input
The first and only line in the input contains a single
integer N , representing
the interior sidelength of the square.

## Output
Output a square of size N
× N . Note that the number of spaces in the output
must be exactly correct and if there are any spaces outside the
square then your solution will be considered incorrect.

## Scoring
### Sample 1
**Input**
```text
0
```
**Output**
```text
++
++
```

### Sample 2
**Input**
```text
1
```
**Output**
```text
+-+
| |
+-+
```

### Sample 3
**Input**
```text
2
```
**Output**
```text
+--+
|  |
|  |
+--+
```
