You’re creating problems for competitive
programming practical examination, but you’re told your
problems are either too hard or too easy. Fortunately, you’ve
got 99 problems and coming up with more ain’t one. To decide on
suitable problems, you will discard problems based on their
difficulty.

After coming up with N problems of difficulty D_ i , you will be told
to discard either

- The easiest problem strictly harder
than difficulty D . If you have problems of
difficulties [10, 10,
11] and students find D = 10 too hard, you will
discard D_ i = 11 to
get [10, 10] .
- The hardest problem not harder
than difficulty D . If you have problems of
difficulties [10, 10,
11] and students find D = 10 too easy, you will
discard the last D_ i =
10 to get [10,
11] .

## Input
The first line contains two integers N ( 1
≤ N ≤ 5 × 10^5 ) and Q ( 1
≤ Q ≤ 10^5 ).

The next line contains N integers of D_ i ( 1 ≤ D_ i ≤ 10^9 ), the
difficulties of the N problems you came up with.

The next Q lines
contain two integers T ( 1 or 2 ) and D ( 1
≤ D ≤ 10^9 ). T corresponds to discarding problems strictly harder than ( 1 ) or not harder
than ( 2 ) D .

## Output
For each problem discarded, print the difficulty D_ i of the problem on a
new line. If a problem of the required difficulty does not
exist or was previously discarded, print -1 .

## Subtasks
- ( 1 Points ): Sample Input.
- ( 18 Points ): N ≤ 10^4 , Q ≤ 10^4 , D ≤ 10^3 and T = 1 .
- ( 22 Points ): N ≤ 10^4 , Q ≤ 10^4 and D_ i ≤ 10^3 .
- ( 19 Points ): Q ≤ 10^4 and D_ i ≤ 10^3 .
- ( 25 Points ): Q ≤ 10^4 and D_ i are unique.
- ( 15 Points ): No additional
constraints.

## Warning
The I/O files are large. Please use fast I/O methods.

### Sample 1
**Input**
```text
3 4
10 10 11
1 10
1 10
1 9
1 5
```
**Output**
```text
11
-1
10
10
```

### Sample 2
**Input**
```text
3 4
10 10 11
2 10
2 10
2 10
2 15
```
**Output**
```text
10
10
-1
11
```
