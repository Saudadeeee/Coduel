Being educated in Computer Science and Mathematics is not
always easy. Especially not if you have “friends” who
repeatedly insist on showing you their new “proofs” that P
equals NP, that the Riemann Hypothesis is true, and so on.

One of your friends recently claims to have found a
fantastic new compression algorithm. As an example of its
amazing performance, your friend has told you that every file
in your precious collection of random bit strings after
compression would be at most b bits long! Naturally, you find
this a bit hard to believe, so you want to determine whether it
is even theoretically possible for this to be true.

Your collection of random bit strings consists of N files, no two of which
are identical, and each of which is exactly 1000 bits long.

## Input
The input consists of two integers N ( 1
≤ N ≤ 10^15 ) and b ( 0
≤ b ≤ 50 ), giving the number of files in your
collection and the maximum number of bits a compressed file is
allowed to have.

## Output
Output a line containing either “ yes ” if it is possible to compress all the N files in your
collection into files of size at most b bits, or “ no ” otherwise.

### Sample 1
**Input**
```text
13 3
```
**Output**
```text
yes
```

### Sample 2
**Input**
```text
1 0
```
**Output**
```text
yes
```

### Sample 3
**Input**
```text
31415926535897 40
```
**Output**
```text
no
```
