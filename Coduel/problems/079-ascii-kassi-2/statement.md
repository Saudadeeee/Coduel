![/problems/asciikassi2/file/statement/en/img-0001.png](https://open.kattis.com/problems/asciikassi2/file/statement/en/img-0001.png)
Image from wikimedia.commons.org

Last year we looked back in time and made contestants draw
ASCII boxes as a challenge. This year we want to look at things
from a new perspective! Therefore the challenge this year is to
draw an ASCII box, but diagonally!

Last time the symbols + , - and | were used to draw the box. When this has been rotated by 45^circ you get the
symbols x , / and \ . The corners
of the box are therefore drawn with a x and the other symbols are used for the
sides.

To make sure the box is printed correctly you need to put
the right number of spaces before and between the symbols on
each line. The last non-whitespace character should be
immediately followed by a newline character. Additionally you
must not print any extra spaces after the box on any line. The
first line of the box is therefore always some number of spaces
followed by a single x . Next there is
a line that has a / below and to the
left of the x and a \ below and to the right of the x , unless the side length of the box is 0 . This continues until
the sides have the correct length. Finally there is a line with
a x below and to the left of the last / and another x below and to the right of the \ . This is then repeated in a mirrored way to
make the bottom half of the box.

## Input
The first and only line of the input contains a single
integer n , the side
length of the box.

## Output
Print a box with side length n as described above. Be aware that
the output must match exactly, even the whitespace
characters.

## Scoring
### Sample 1
**Input**
```text
0
```
**Output**
```text
x
x x
 x
```

### Sample 2
**Input**
```text
1
```
**Output**
```text
x
 / \
x   x
 \ /
  x
```

### Sample 3
**Input**
```text
2
```
**Output**
```text
x
  / \
 /   \
x     x
 \   /
  \ /
   x
```
