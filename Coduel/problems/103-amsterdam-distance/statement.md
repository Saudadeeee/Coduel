Your friend from Manhattan is visiting you in Amsterdam.
Because she can only stay for a short while, she wants to see
as many tourist attractions in Amsterdam in as little time as
possible. To do that, she needs to be able to figure out how
long it takes her to walk from one landmark to another. In her
hometown, that is easy: to walk from point m = (m_ x, m_ y) to point n = (n_ x, n_ y) in
Manhattan you need to walk a distance

since Manhattan looks like a rectangular grid of city
blocks. However, Amsterdam is not well approximated by a
rectangular grid. Therefore, you have taken it upon yourself to
figure out the shortest distances between attractions in
Amsterdam. With its canals, Amsterdam looks much more like a
half-disc, with streets radiating at regular angles from the
center, and with canals running the arc of the circle at
equally spaced intervals. A street corner is given by the
intersection of a circular canal and a street which radiates
from the city center.

Depending on how accurately you want to model the street
plan of Amsterdam, you can split the city into more or fewer
half rings, and into more or fewer segments. Also, to avoid
conversion problems, you want your program to work with any
unit, given as the radius of the half circle. Can you help your
friend by writing a program which computes the distance between
any two street corners in Amsterdam, for a particular
approximation?

## Input
The input consists of

- One line with two integers M,N and a real number R . 1 ≤ M ≤
100 is the number of segments (or ‘pie slices’)
the model of the city is split into. 1 ≤ N ≤
100 is the number of half rings the model of
the city is split into. 1 ≤ R ≤
1000 is the radius of the city, given with at
most 15 digits
after the decimal point.
- One line with four integers, a_ x, a_ y, b_ x, b_ y , with 0 ≤ a_ x, b_ x ≤
M , and 0 ≤ a_ y,
b_ y ≤ N , the coordinates of two corners in the
model of Amsterdam.

## Output
Output a single line containing a single real number, the
least distance needed to travel from point a to point b following only the streets in the
model. The result should have an absolute or relative error of
at most 10^-6 .

### Sample 1
**Input**
```text
6 5 2.0
1 3 4 2
```
**Output**
```text
1.65663706143592
```

### Sample 2
**Input**
```text
9 7 3.0
1 5 9 5
```
**Output**
```text
4.28571428571429
```

### Sample 3
**Input**
```text
10 10 1.0
2 0 6 0
```
**Output**
```text
0
```
