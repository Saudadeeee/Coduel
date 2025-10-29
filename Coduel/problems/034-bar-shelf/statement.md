![/problems/barshelf/file/statement/en/img-0001.png](https://open.kattis.com/problems/barshelf/file/statement/en/img-0001.png)
A perfectly civilised arrangement of bottles. Detail from Dictionnaire encyclopédique de l’épicerie et des
industries annexes by Albert Seigneurie, 1904,
p. 117. Public domain.

Organ pipes, the von Trapp children, staircases—oh, how
Quark loves these things. For they are neatly arranged
ascending order, the very signal of cleanliness, structure, civilisation . Quark is your fellow bartender at Meson , the longest bar in the galaxy. Were it up to
Quark, the bottles on the bar shelf would all be neatly and
properly ordered, left-to-right, and in ascending order.

You disagree with Quark. As far as you can tell, the bar’s
patrons appreciate Meson ’s welcoming atmosphere of
carefully orchestrated insouciance. Surely, a certain amount
messiness on the bar shelf is important for that image.

This has led to long discussions between you and Quark about
how messy the shelf can be. He concedes that a bottle placed to
the left of one that is just slightly smaller doesn’t look very
messy at all. On the other hand, you have to admit that very
big size differences do look way too messy. Finally, you have
agreed on the following rule: Three bottles, not necessarily
adjacent, are a messy trio if the one to the left is
at least twice as large as the middle one, which in turn is at
least twice as large as the one to the right.

For instance, in the image below, the bottles have height 4 , 5 , 2 , 1 , and 3 , from left to right. The bottles
of height 4 , 2 , and 1 form a messy trio (because frac12 · 4 ≥ 2≥
2· 1 ), and so do 5 , 2 , and 1 . The messiness of the entire shelf
is the number of messy trios, in this case 2 .

## Input
The input consists of two lines. On the first line, the
number n of bottles on
the shelf, with n≥ 1 .
On the second line, n integers, separated by space, giving the height (in nanometres)
of each bottle from left to right. Each height is an integer
between 1 and 10^9 .

## Output
Output a single integer: the messiness of the shelf. Note
that this number can be quite large, but no larger than binom n3 , which for
our largest input is bounded by 2 · 10^15 .

## Scoring
Your score depends on the length of the shelf that you can
handle within the time limit. You get one point for n≤ 100 , another for n≤ 5 000 , and yet
another for n≤ 200 
000 . The maximum score is 3 points.

### Sample 1
**Input**
```text
5
4 5 2 1 3
```
**Output**
```text
2
```

### Sample 2
**Input**
```text
4
10 5 5 2
```
**Output**
```text
2
```

### Sample 3
**Input**
```text
3
1 2 4
```
**Output**
```text
0
```
