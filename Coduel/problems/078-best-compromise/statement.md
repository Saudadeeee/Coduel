![/problems/compromise/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/compromise/file/statement/en/img-0001.jpg)
Photo by Andy
Nelson

There is a saying “a good compromise makes no one happy”. As
distressing as that may be, I guess most people still think it
is a good idea to seek the best agreement. The problem though,
is to define the measure in which the word “best” gets a
meaning. Let us consider n people, each with a firm belief on m different yes/no
issues. We may think of the people’s beliefs as binary strings b_ i of length m for 0<i≤ n , i.e. one string per
person, with entries reflecting a person’s belief in each of
the m issues. An agreement is also a binary string a of length m , indicating the agreed outcome of
each of the m issues.
Some would argue that the agreement a that minimises the maximum of H(b_ i-a) over all i , where H(x) is the Hamming function
counting the number of non-zero entries of the vector x , is the best
compromise. Unfortunately, it is widely believed that finding
this agreement is computationally infeasible for n and m large. Another reasonable
suggestion is the agreement a that minimises (sum _i=1^ n H(b_ i-a)^
p)^1/p for some positive integer p . Note in particular that when parrow infty ,
this measure coincides with the former. I for one am most
content with the choice of p=1 though, don’t you agree?

## Input
On the first line of input is a single positive integer t , telling the number of
test scenarios to follow. Each test scenario is described by
two positive integers n≤
100 and m≤
100 , on a line of their own. Then follow n lines, each containing a binary
string b_ i on m ‘0’ and ‘1’
characters.

## Output
For each test scenario, output the assignment a that minimises the measure above
with p = 1 , on a row of
its own. If there are several solutions, output anyone.

### Sample 1
**Input**
```text
2
5 5
00000
00100
01001
01101
00101
1 7
0110010
```
**Output**
```text
00101
0110010
```
