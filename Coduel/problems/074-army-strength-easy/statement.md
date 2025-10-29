Note that this is an easier version of the problem
armystrengthhard.

The next MechaGodzilla invasion is on its way to Earth. And
once again, Earth will be the battleground for an epic war.
MechaGodzilla’s army consists of many nasty alien monsters,
such as Space Godzilla, King Gidorah, and MechaGodzilla
herself. To stop them and defend Earth, Godzilla and her
friends are preparing for the battle.

Each army consists of many different monsters. Each monster
has a strength that can be described by a positive integer. The
larger the value, the stronger the monster. The war will
consist of a series of battles. In each battle, the weakest of
all the monsters that are still alive is killed. If there are
several weakest monsters, but all of them in the same army, one
of them is killed at random. If both armies have at least one
of the weakest monsters, a random weakest monster of
MechaGodzilla’s army is killed. The war is over if in one of
the armies all monsters are dead. The dead army lost, the other
one won. You are given the strengths of all the monsters. Find
out who wins the war.

## Input
The first line of the input file contains an integer T≤ 50 specifying the
number of test cases. Each test case is preceded by a blank
line.

Each test case starts with line containing two positive
integers N_ G and N_ M – the number of
monsters in Godzilla’s and in MechaGodzilla’s army. You can
assume that N_ G, N_ M≤
500 .

Two lines follow. The first one contains N_ G positive integers – the
strengths of the monsters in Godzilla’s army. Similarly, the
second one contains N_ M positive integers – the strengths of the monsters in
MechaGodzilla’s army. All strengths are at most 10 000 .

## Output
For each test case, output a single line with a string that
describes the outcome of the battle. If it is sure that
Godzilla’s army wins, output the string “ Godzilla ”. If it is sure that MechaGodzilla’s army
wins, output the string “ MechaGodzilla ”.
Otherwise, output the string “ uncertain ”.

### Sample 1
**Input**
```text
2

1 1
1
1

3 2
1 3 2
5 5
```
**Output**
```text
Godzilla
MechaGodzilla
```
