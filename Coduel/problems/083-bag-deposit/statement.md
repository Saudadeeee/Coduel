Tim manages a bag deposit counter. In the morning, people
would stop by at his counter to deposit their bags before they
go on to do their daily business. They will then come back to
collect the bags in the evening each at different times. When
people deposit their bags, they will be given a unique id tag
for the bag and they need to indicate the time that they will
be back to collect their bags. His business has been doing
really well but there is one major problem. There are more than 100 bags each day and
Tim can’t just be looking for the bag in the large piles of
bags. To optimize his operation he will need to find a way to
stack the bags such that he can place them on the stack as they
come in and pick the bag from the top of the stack whenever
people come back to collect the bags, instead of trying to dig
under the pile. And due to limited space, he will need to
minimize the number of stacks. There is no limit on how high
the stack can be and all the customers will have deposited
their bags before anyone comes back to collect their bag.

## Input
Input begins with a line containing an integer n representing the number of bags.
The next n lines each
represents one bag ordered chronologically (so the first bag
checked in precedes the second bag checked in, etc.). Each line
contains a 4-digit unique bag id followed by the order r , ( 0 ≤ r < 10000 ) in which the
bag will be collected. For example 2342 5 represents bag with id 2342 and is the sixth
bag that will be collected, where 0 is the first bag to be
collected.

## Output
Output the minimal number of stacks needed so that as the
bags are collected, they will only be taken from the top of the
stack.

### Sample 1
**Input**
```text
5
0001 4
0002 3
0003 5
0004 1
0005 2
```
**Output**
```text
2
```

### Sample 2
**Input**
```text
10
0000 1
0001 6
0002 8
0003 2
0004 0
0005 5
0006 3
0007 7
0008 9
0009 4
```
**Output**
```text
5
```
