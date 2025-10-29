In his unending goal to become the greatest programmer of
all time, Gustav has decided to go to Singapore. Curiosity
leads him into the game room, where some of his new friends are
playing cards. "What game are you playing?" he asks. His
friends go on to tell him about a seemingly ancient
mathematical card game called twenty four. The goal is to
create the number T ,
typically 24 , using only
the numbers on the C cards placed on the table, the four basic arithmetic operators
(+,-,*,/) and parentheses. Gustav can also change the order of
the cards. Note that unary operators are not allowed (i.e., 1 · -2 is invalid).
Cards with numbers on them take on that value. Ace represents
one, Jack represents 11 ,
Queen represents 12 and
King represents 13 .

Since Gustav’s new friends are incredibly experienced and
beat him every single round, help him write a program that can
play for him.

## Input
The first line contains two positive integers C and T ( 1
≤ C ≤ 6 , 1 ≤
10^3 ), the number of cards and the target number
respectively. The second line contains C integers c_1, c_2, … c_ C ( 1 ≤ c_ i ≤ 13 ), the cards placed
on the table.

## Output
Print any solution that equals T . There is guaranteed to exist at
least one solution.

## Points
Your solution will be tested on several test case groups. To
get the points for a group, it must pass all the test cases in
the group.

### Sample 1
**Input**
```text
4 24
1 12 1 12
```
**Output**
```text
(((12-1)+12)+1)
```

### Sample 2
**Input**
```text
4 24
1 2 3 4
```
**Output**
```text
(((4*3)*2)*1)
```

### Sample 3
**Input**
```text
4 24
3 3 8 8
```
**Output**
```text
(8/(3-(8/3)))
```
