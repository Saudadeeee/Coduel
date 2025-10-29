![/problems/bergur/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/bergur/file/statement/en/img-0001.jpg)
Hot Yoga

Bergur has decided to go to a Hot Yoga class to burn some
fat. Bergur doesn’t think it’s good enough to just regularly
attend Hot Yoga classes, he wants to always stay at least as
long as he did the previous day. That is to say, Bergur intends
to show up for Hot Yoga every day for the next N days. You are given for each day,
how long he can be in Hot Yoga class, defined as a_ i for the i -th day. He is welcome to leave
earlier than that.

Bergur wants to spend the maximum amount of time possible in
Hot Yoga classes over these N days but still satisfy the
requirement of staying at least as long as the previous day
every time.

That is to say, the amount of time Bergur spends on Hot Yoga
over the days is non-decreasing.

## Input
The first line of the input contains one integer N ( 1 ≤ N ≤ 3 · 10^5 ), the
number of days.

The next line contains N integers 1 ≤ a_ i ≤ 10^4 where the i -th number denotes the
maximum amount of time Bergur can stay in class that day.

## Output
Print a single integer, the maximum amount of time Bergur
can spend in Hot Yoga classes in total while still satisfying
the requirements described above.

## Scoring
### Sample 1
**Input**
```text
10
5 6 7 8 9 3 2 7 8 9
```
**Output**
```text
38
```

### Sample 2
**Input**
```text
3
3 2 1
```
**Output**
```text
3
```
