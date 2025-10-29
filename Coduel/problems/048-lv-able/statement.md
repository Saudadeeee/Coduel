A string is “ lv ”-able if it
contains the contiguous substring “ lv ”.

You are given a string s with N characters, and you want to make
it “ lv ”-able in as few operations as
possible.

You are allowed to do any of these operations:

- Remove any character at any position.
- Insert any character at any position.
- Replace any character by any other character at any
position.
- Choose any consecutive interval of characters, and
reverse the order of the characters in it.

Now make the string “ lv ”-able!

## Input
The first line of input contains an integer N ( 1
≤ N ≤ 5 · 10^5 ), the number of characters in
the initial string.

The second line contains the string s , which consists of N lowercase letters a - z .

## Output
Print an integer: the minimum number of operations such that
the string s becomes
“ lv ”-able.

## Scoring
Your solution will be tested on a set of test groups, each
worth a number of points. Each test group contains a set of
test cases. To get the points for a test group you need to
solve all test cases in the test group.

## Explanation of Samples
In sample 1 , you can
reverse the substring “ ov ”, resulting
in lvoable , which then contains
“ lv ”.

In sample 2 , we can
replace the “ e ” with a “ v ”, which then contains “ lv ”.

In sample 3 , the
string already contains “ lv ”.

### Sample 1
**Input**
```text
7
lovable
```
**Output**
```text
1
```

### Sample 2
**Input**
```text
6
google
```
**Output**
```text
1
```

### Sample 3
**Input**
```text
6
lvable
```
**Output**
```text
0
```
