![/problems/3puzzle/file/statement/en/img-0001.png](https://open.kattis.com/problems/3puzzle/file/statement/en/img-0001.png)
Photo by Booyabazooka. Retrieved from
commons.wikimedia.org. Public Domain. Source

Your friend needs help solving a 15 -Puzzle, so to warm up, you solve
the 3 -Puzzle instead. A 3 -Puzzle consists of a 2 × 2 grid
containing 3 tiles
numbered 1 through 3 and one empty space.
The goal is to slide the tiles around so that they are in
ascending row-major order and the empty space is on the bottom
right like this:

Given the starting position of a 3 -Puzzle, find the minimum number of
moves it takes to solve the puzzle. Here’s an example of how
sample input 1 can be
solved in 3 moves:

Starting position:

After 1 move:

After 2 moves:

After 3 moves:

## Input
The input will consist of exactly 2 lines, each containing exactly 2 characters.

Each character is either a number 1 through 3 (representing one of the tiles) or
a dash ( - ) (the empty space).

The puzzle state represented by the input is guaranteed to
be a solvable configuration.

## Output
Output a singe integer, indicating the minimum number of
moves required to solve the puzzle from the provided starting
position, or 0 if it’s
already in the solved position.

### Sample 1
**Input**
```text
2-
13
```
**Output**
```text
3
```

### Sample 2
**Input**
```text
-3
21
```
**Output**
```text
6
```
