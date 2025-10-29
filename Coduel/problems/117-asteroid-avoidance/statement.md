The legendary starship of Flatland, Rectalateral, needs to
escape from a star which is about to go supernova by
teleporting away. Unfortunately, the possible teleport
destinations are in the middle of an asteroid field. Luckily,
you have a map of the asteroid field with the exact radius and
location of the asteroids (asteroids in Flatland are circles,
obviously). As the navigator on board, you must investigate
each of the possible teleport destinations and determine if
they are safe.

A teleportation destination is safe if and only if no
asteroid would touch or overlap Rectalateral immediately after
the teleportation completes. Rectalateral will be axis-aligned
after the teleportation (the sides of Rectalateral are parallel
to the x -axis or the y -axis).

## Input
The first line of input is two integers 1≤ w, h ≤ 100 , the width and
height of the rectangular Rectalateral.

The second line of input is two integers n, m , where 1 ≤ n ≤ 100 is the number of
asteroids in the asteroid field, and 1 ≤ m ≤ 100 is the number of
potential teleportation destinations.

The next n lines are
each three integers x_ a , y_ a
, r_ a , where -1000 ≤
x_ a , y_ a ≤ 1000 is the location of the center of
the circular asteroid and 1 ≤
r_ a ≤ 100 is the radius of the asteroid.

The next m lines are
each two integers x_ r,y_
r , where -1000 ≤ x_
r,y_ r ≤ 1000 is the location of the bottom-left
corner of Rectalateral after the teleport. (This means that the
top-right corner will be at (x_
r + w, y_ r + h) .)

The x -axis increases
rightwards, and the y -axis increases upwards.

## Output
For each potential teleportation destination, in the order
the teleportation destinations were given, output a single line
“ DOOMSLUG GO! ” if the teleport destination is safe,
otherwise output a single line “ DOOMSLUG STOP! ”.

### Sample 1
**Input**
```text
1 1
2 4
0 0 10
7 9 1
8 6
8 7
8 9
0 0
```
**Output**
```text
DOOMSLUG STOP!
DOOMSLUG GO!
DOOMSLUG STOP!
DOOMSLUG STOP!
```
