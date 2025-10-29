Congratulations! You’ve just inherited a treasure map from a
long deceased ancestor who just happened to be a pirate. With
visions of gold doubloons and jeweled cutlasses dancing in your
head you carefully unfold the map. However instead of the
standard picture map with a large X where the treasure is, this
map is simply a list of instructions on where to start digging.
The first instruction is the starting location, given as two
integers x y giving the starting point’s
latitude and longitude. After this are instructions like N 7 or
SW 6 which specify to walk 7 feet north or 6 feet southwest.
After following all of these instructions you will be located
over the spot to start digging.

(Just to be clear, moving north increases the y value of your location and keeps
the x value constant;
moving east increases the x value of your location and keeps
the y value constant.
You can determine the effects the other directions have on the
location.)

Now, you could go through the laborious task of executing
each of the instructions one at a time, starting at the initial
location, but it would be a lot easier to just calculate the
final location and head right there. And that’s the task for
this problem.

Oh, one more thing: turns out your ancestor was actually a
Pittsburgh Pirate, and the treasure consists of a bunch of old
baseballs and a really moldy mitt. I’m sure you can get a
doubloon or two for them on eBay.

## Input
Input starts with a line containing a single integer n ( 1 ≤ n ≤ 100 ) indicating the
number of instructions. The next n lines each contain a single
instruction. The first instruction consists of two integers x y ( 0
≤ x,y ≤ 100 ) indicating the starting point. The
remaining instructions are of the form dir d , were dir is the direction (either N, NE, E,
SE, S, SW, W or NW ) and d ( 1
≤ d ≤ 100 ) is the distance to walk.

## Output
Display the x and y coordinates of the
final location, separated by a single space. All coordinates
should have a maximum relative or absolute error of 10^-6 .

### Sample 1
**Input**
```text
3
5 5
N 10
W 7
```
**Output**
```text
-2.00000000 15.00000000
```

### Sample 2
**Input**
```text
3
0 0
NE 10
SE 7
```
**Output**
```text
12.02081528 2.12132034
```
