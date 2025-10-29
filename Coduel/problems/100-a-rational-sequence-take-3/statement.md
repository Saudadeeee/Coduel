A sequence of positive rational numbers is defined as
follows:

An infinite full binary tree labeled by positive rational
numbers is defined by:

- The label of the root is 1/1 .
- The left child of label p/q is p/(p+q) .
- The right child of label p/q is (p+q)/q .

The top of the tree is shown in the following figure:

The sequence is defined by doing a level order (breadth
first) traversal of the tree (indicated by the light dashed
line). So that:

Write a program to compute the n^text th element of the
sequence, F(n) . Does
this problem sound familiar? Well it should! We had variations
of this problem at the 2014 and 2015 Greater NY ACM ICPC
Regionals.

## Input
The first line of input contains a single integer P , ( 1 ≤ P ≤ 1 000 ), which is the
number of data sets that follow. Each data set should be
processed identically and independently. Each data set consists
of a single line of input. It contains the data set number, K , and the index, N , of the sequence
element to compute ( 1 ≤ N ≤
2 147 483 647 ).

## Output
For each data set there is a single line of output. It
contains the data set number, K , followed by a single space which
is then followed by the numerator of the fraction, followed
immediately by a forward slash (‘ / ’)
followed immediately by the denominator of the fraction. Inputs
will be chosen so neither the numerator nor the denominator
will overflow an 32 -bit unsigned integer.

### Sample 1
**Input**
```text
4
1 1
2 4
3 11
4 1431655765
```
**Output**
```text
1 1/1
2 1/3
3 5/2
4 2178309/1346269
```
