![/problems/beehives/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/beehives/file/statement/en/img-0001.jpg)

Bill the beekeeper has a problem! His bees like to fight
with each other instead of producing honey. If the bees fight
each other, then the honey turns out sour. The only way to stop
the bees from fighting and keep the honey sweet is to ensure
that the hives are not too close together. Help Bill figure out
how many of this season’s hives will produce sour honey.

Bill’s hives all exist on a plane, and he knows some
distance d such that two hives within d of each other will fight, and both
will produce sour honey. If a hive does not fight with any
other hives, it produces sweet honey. Given d and the positions of N beehives, output how many hives
will produce sweet honey and how many hives will produce sour
honey.

## Input
Input will be provided on multiple lines. There may be up to 10 test cases in the
input. Each case will begin with a floating point number d ( 0 < d < 1000 ), the distance
within which hives will fight, followed by an integer N ( 1 ≤ N ≤ 100 ), the number of
hives in that case. The next N lines will contain two floating
point numbers separated by a single space, x and y ( -1000 ≤ x,y ≤ 1000 ), which give
the position of each hive. No two hives will be at the exact
same location. Input will be terminated by a line containing
the string 0.0 0 .

## Output
For each case output a line of the following form: a sour, b sweet where a and b are the number of hives producing
sour and sweet honey, respectively.

### Sample 1
**Input**
```text
10.0 3
3.0 3.0
3.5 4.5
20.0 20.0
5.0 4
2.0 1.0
2.0 4.0
2.0 8.0
2.0 12.0
0.0 0
```
**Output**
```text
2 sour, 1 sweet
4 sour, 0 sweet
```
