![/problems/barcelona/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/barcelona/file/statement/en/img-0001.jpg)
Image from flickr.com

Arnar, Benni and Unnar were at the airport in Barcelona on
their way to a competitive programming training camp. When the
plane had landed they exited and went to the baggage claim.
When they arrived there was no baggage on the conveyor belts.
After a few minutes the baggage started trickling in. When
Benni noticed this he loudly proclaimed “My bag’s first! No,
it’s second first! No... it’s fourth first. No wait...”

Given a list of bags and a number denoting Benni’s bag, can
you help Benni find how first his bag is?

## Input
First there is a line with two integers n and k , the number of bags and Benni’s
bag. It will always hold that 1
≤ n ≤ 10^5 and -10^9 ≤ k ≤ 10^9 . Next there
is a line with n integers separated by spaces, a_1, a_2, …c , a_ n . For each 1 ≤ i ≤ n it holds
that -10^9 ≤ a_ i ≤
10^9 . No two bags are given by the same number and
Benni’s bag always appears in the list.

## Output
Print a single line. If Benni’s bag is first print fyrst , if it’s the second print naestfyrst . Otherwise print a single
number denoting how first it is followed by the word fyrst after the number.

## Scoring
### Sample 1
**Input**
```text
8 0
0 -1 2 -3 4 -5 6 -7
```
**Output**
```text
fyrst
```

### Sample 2
**Input**
```text
5 42
1337 42 -6 9 420
```
**Output**
```text
naestfyrst
```

### Sample 3
**Input**
```text
7 7
1 2 3 4 5 6 7
```
**Output**
```text
7 fyrst
```
