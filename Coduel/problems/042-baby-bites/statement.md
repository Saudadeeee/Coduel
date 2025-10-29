![/problems/babybites/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/babybites/file/statement/en/img-0001.jpg)

Arild just turned

year old, and is currently
learning how to count. His favorite thing to count is how many
mouthfuls he has in a meal: every time he gets a bite, he will
count it by saying the number out loud.

Unfortunately, talking while having a mouthful sometimes
causes Arild to mumble incomprehensibly, making it hard to know
how far he has counted. Sometimes you even suspect he loses his
count! You decide to write a program to determine whether
Arild’s counting makes sense or not.

## Input
The first line of input contains an integer n ( 1
≤ n ≤ 1 000 ), the number of bites Arild receives.
Then second line contains n space-separated words spoken by
Arild, the i ’th of which
is either a non-negative integer a_ i ( 0 ≤ a_ i ≤ 10 000 ) or the
string “ mumble ”.

## Output
If Arild’s counting might make sense, print the string
“ makes sense ”. Otherwise, print the
string “ something is fishy ”.

### Sample 1
**Input**
```text
5
1 2 3 mumble 5
```
**Output**
```text
makes sense
```

### Sample 2
**Input**
```text
8
1 2 3 mumble mumble 7 mumble 8
```
**Output**
```text
something is fishy
```

### Sample 3
**Input**
```text
3
mumble mumble mumble
```
**Output**
```text
makes sense
```
