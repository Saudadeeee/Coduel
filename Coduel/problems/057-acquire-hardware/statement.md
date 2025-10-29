![/problems/acquirehardware/file/statement/en/img-0001.png](https://open.kattis.com/problems/acquirehardware/file/statement/en/img-0001.png)
Iron Ingot, Minecraft Wiki

Kai is tasked with gathering iron to make tools and armor.
She looks from the top of a nearby hill and sees a rectangular
field and tries to plan out a single path through the field
that will allow her to collect the most iron.

Kai will begin in the top-left corner of the field and
considers only right and down as allowable
moves. Kai’s goal is to determine the maximum number of iron
blocks that can be picked up in a single path (again only right and down are allowed) traversing to the
bottom-right corner of the field. Can you help Kai figure out
this maximum number of iron blocks that can be collected in a
single pass?

## Input
The first line of the input contains two integers, h and w , the height and width of the
field. You are given that 1 ≤
h,w ≤ 500 . The next h lines each contain a string of w characters describing
one row of the rectangular field. Each character will be an
upper-case letter describing the type of block that is present
at that location; the letter I represents a block of iron. There will be no iron on the
top-left starting square but there may be on the bottom-right
destination square. The top-left and bottom-right squares will
be distinct (there will be at least 2 squares).

## Output
Output a single integer, the maximum number of iron blocks
that can be obtained in a single pass from top-left to
bottom-right.

### Sample 1
**Input**
```text
3 4
HBIS
IYAI
IUIC
```
**Output**
```text
3
```
