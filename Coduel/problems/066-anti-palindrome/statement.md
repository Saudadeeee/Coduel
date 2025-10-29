![/problems/antipalindrome/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/antipalindrome/file/statement/en/img-0001.jpg)

A palindrome is a sequence of two or more characters that
reads the same both forward and backward. Palindromes can
appear inside a longer text, such as “Happy days are here
again.” in which “pp”, “ehe” and “ere” are some of the
palindromes (ignoring spaces, punctuation, and case). An
anti-palindrome is a sequence of two or more characters in
which there are no palindromes. You are given text that may
contain, or itself form, a palindrome. Your task is to
determine if there are any palindromes in the text, in which
case declare "Palindrome", or if there are none, declare
"Anti-palindrome". The text may contain spaces, as well as
alphabetic and other non-alphabetic characters. All
non-alphabetic characters should be ignored, and uppercase and
lowercase letters are considered the same when detecting
palindromes.

## Input
The input consists of one line of text as specified above.
The input line will not be longer than 80 characters, and
contains at least one alphabetic character.

## Output
Print “Palindrome" if the text contains or is itself a
palindrome, or “Anti-palindrome" if there are no palindromes in
the text.

### Sample 1
**Input**
```text
Happy days are here again.
```
**Output**
```text
Palindrome
```

### Sample 2
**Input**
```text
It is game day.
```
**Output**
```text
Palindrome
```

### Sample 3
**Input**
```text
It was game day.
```
**Output**
```text
Anti-palindrome
```
