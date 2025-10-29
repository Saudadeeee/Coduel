![/problems/ball/file/statement/en/img-0001.png](https://open.kattis.com/problems/ball/file/statement/en/img-0001.png)
Image from commons.wikimedia.org

There is a school dance scheduled tomorrow and n students will attend. The students
are numbered from 1 to n . The students are
registered in pairs and the list of attendees is fracn2 + 1 lines long. Each
number also appears once in the list. But that doesn’t add up!
Some devious prankster must have added a pair to the list
somewhere. Given the list determine which pair should be
removed.

## Input
The first line of the input contains a single even integer n ( 2 ≤ n ≤ 2 · 10^5 ), the
number of students. Then follow fracn2 + 1 lines. Each line
contains two integers a_ i, b_
i ( 1 ≤ a_ i, b_ i
≤ n ), indicating the i -th pair on the list.

## Output
Print the pair that the prankster added, on a single line.
The numbers, a and b , should be separated
by a single space and ordered such that a < b .

## Scoring
### Sample 1
**Input**
```text
10
1 2
3 5
4 8
6 7
4 7
9 10
```
**Output**
```text
4 7
```

### Sample 2
**Input**
```text
2
2 1
1 2
```
**Output**
```text
1 2
```
