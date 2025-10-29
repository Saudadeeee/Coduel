Have you ever wondered what the average ASCII character of
any given string is? No? Never? Really? Well, is it a character
in the string or something else?

Would you do this calculation by hand with an ASCII table?
Probably not! All modern programming languages include
functions for converting an ASCII character to an integer, and
to convert an integer to an ASCII character. Of course, these
functions often also handle unicode characters as well, but
that is not part of this problem.

Given a string of ASCII characters, compute the average
character. If the average character lies between two integer
ASCII values, return the smaller one.

## Input
The single line of input contains a single string s ( 1 ≤ |s| ≤ 100 ), which consists
of ASCII text. All of the characters of s will be printable ASCII, between
ASCII 32 (space: ‘ ’ ) and ASCII 126 (tilde: ‘ ’ ). It will NOT contain any control characters such as carriage returns, line
feeds, tabs, etc. It is NOT guaranteed
to begin, end, or even contain a non-space character.

## Output
Output a single ASCII character, which is the average of all
of the ASCII characters in s .

### Sample 1
**Input**
```text
ABCDE
```
**Output**
```text
C
```

### Sample 2
**Input**
```text
AbCdE
```
**Output**
```text
O
```

### Sample 3
**Input**
```text
aBcDe
```
**Output**
```text
V
```
