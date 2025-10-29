![/problems/1dfroggereasy/file/statement/en/img-0001.png](https://open.kattis.com/problems/1dfroggereasy/file/statement/en/img-0001.png)
Image by alptraum (iStock) ; Used under license

Frogger is a classic 2 -D video
game that challenges the player to move a frog character safely
across a traffic-filled road and a hazardous river. What is not
well known is that Frogger actually began as a prototype board
game based on a 1 -D concept at a now-defunct
toy company. 1 After spending millions of dollars
following the advice of consultants, company executives
realized that the resulting game was almost completely
deterministic, and therefore not much fun to play, 2 so they sold all Frogger rights to a
video game company in an attempt to recoup some of the
development costs. The rest, as they say, is video game
history.

The original 1 -D Frogger design, however,
makes for good programming competition problems. Here is how
the game works. The board is a row of n squares, each of which contains a
non-zero integer. These squares are indexed 1, 2, … , n , from left to
right. To start the game, the player rolls an n -sided die with one of the
distinct indices on each side, and places a frog token on the
board square with the resulting index. The player then randomly
selects a card from a deck of cards with integers written on
them (one per card); the integer on each card is contained in
at least one board square. The number on the selected card is
the magic number (or goal number ) for this
instance of the game.

The player then applies the following rule as many times as
necessary until the game ends:

- If the frog is on a square containing a positive
integer, k , the frog
makes a length- k hop to the right. (Hop
distance is measured in board square units.)
- If the frog is on a square containing a negative
integer, k , the frog
makes a length- |k| hop to the left (note
the absolute value).

The game ends as soon as the frog encounters one of the
following four fates:

- The frog lands on a square containing the magic number.
This is the only winning outcome for the player. Note that
if the frog starts on a square containing the magic number,
the player wins immediately (i.e., after 0 hops).
- The frog falls off the left end of the board.
- The frog falls off the right end of the board.
- The frog hops onto a square where the frog has been
before, and therefore is trapped in a cycle.

Let h ≥ 0 be the
number of hops the frog makes before the game ends. Given an
instance of the game, your task is to determine the frog’s fate
and the corresponding value of h .

## Input
The first line of input contains three space-separated
integers, n , s , m , where n is the number of board squares (1 ≤ n ≤ 200) , s is the index of the
frog’s starting square (1 ≤ s
≤ n) , and m is the magic number. This is followed by a line containing n space-separated
non-zero integers. These are the numbers in the board squares
in order from left to right. Each board square number is in the
interval [-200, 200] ,
and the magic number is guaranteed to be one of the board
square numbers.

## Output
Output two lines. The first line contains a word indicating
the fate of the frog, one of \ ‘ magic ’, ‘ left ’, ‘ right ’,
‘ cycle ’ \ , corresponding to the four fates
listed above, respectively. The second line contains the
integer h , the
number of hops the frog makes before encountering its fate.

### Sample 1
**Input**
```text
6 4 42
-9 1 42 -2 -3 -3
```
**Output**
```text
magic
2
```

### Sample 2
**Input**
```text
8 2 13
7 5 4 2 13 -2 -3 6
```
**Output**
```text
cycle
4
```
