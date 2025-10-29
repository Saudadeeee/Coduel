You are a maintenance worker for a large bank that recently
bought new ATMs. All of them are working flawlessly, except for
a stubborn one on Main Street. It seems to have a limited
amount of money left in the machine, but the system reporting
this number is not working properly. To find out for sure, you
set some volunteers out to try and fix the problem by having
them attempt to withdraw money from their accounts and see if
it works.

Initially, the ATM contains a total of K units of money. N people (numbered 1 through N ) want to withdraw money.

The people come in and try to withdraw money one by one, in
order. Whenever someone tries to withdraw money, if the machine
has at least the required amount of money, it will give out the
required amount. Otherwise, it will throw an error and not give
out anything; in that case, this person will return home
directly without trying to do anything else.

For each person, determine whether they will get the
required amount of money or not.

## Input
The first line of the input contains two space-separated
integers N ( 1 ≤ N ≤ 100 ) and K ( 1
≤ K ≤ 100 000 ). The second line contains N space-separated
integers A_1,A_2,… ,A_
N ( 0 ≤ A_ i ≤ 10 
000 ), corresponding to the amount of money each person
withdraws.

## Output
Output a single line containing a string with length N . For each person, the
i-th character of this string should be 1 if the i-th person will
successfully withdraw their money or 0 otherwise.

### Sample 1
**Input**
```text
5 10
3 5 3 2 1
```
**Output**
```text
11010
```
