![/problems/alphabetspam/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/alphabetspam/file/statement/en/img-0001.jpg)
Photo by Bodo Akdeniz via Wikimedia Commons, GFDL

About

percent
of the 300 billion emails sent every day are spam. Thus, a fast
spam detection mechanism is crucial for large email providers.
Lots of spammers try to circumvent spam detection by rewriting
words like “

”, “

”, or “

”.

A very simple and fast spam detection mechanism is based on
the ratios between whitespace characters, lowercase letters,
uppercase letters, and symbols. Symbols are defined as
characters that do not fall in one of the first three
groups.

## Input
The input consists of:

- one line with a string consisting of at least 1 and at most 100 000 characters.

A preprocessing step has already transformed all whitespace
characters to underscores ( _ ), and the line
will consist solely of characters with ASCII codes between 33
and 126 (inclusive).

## Output
Output four lines, containing the ratios of whitespace
characters, lowercase letters, uppercase letters, and symbols
(in that order). Your answer should have an absolute or
relative error of at most 10^-6 .

### Sample 1
**Input**
```text
Welcome_NWERC_participants!
```
**Output**
```text
0.0740740740740741
0.666666666666667
0.222222222222222
0.0370370370370370
```

### Sample 2
**Input**
```text
\/\/in_US$100000_in_our_Ca$h_Lo||ery!!!
```
**Output**
```text
0.128205128205128
0.333333333333333
0.102564102564103
0.435897435897436
```
