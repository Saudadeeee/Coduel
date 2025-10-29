![/problems/babylonian/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/babylonian/file/statement/en/img-0001.jpg)
Image by Sugarfish ( Wikimedia
Commons ), Public Domain

More than 4 000 years ago, the ancient Babylonians used a numerical system that
is well known for being the first positional numerical system.
In such a system, a non-negative integer is represented by a
sequence of digits such that the value of a digit depends both
on itself and on its position within the sequence. The
Babylonians used a base- 60 system known as sexagesimal (not
unlike our own base- 10 decimal system) where each ‘digit’ can take values between 1 and 59 , inclusive. (The Babylonians
didn’t have a digit to represent 0 ; instead they would just leave the
digit position empty.) Akin to the Egyptians at the time, the
Babylonians carved their equations in solid clay, which allows
us to read them thousands of years later.

Your history professor, Dr. X, has asked you to decipher the
Babylonian numbers he has found during a recent excavation and
to convert them into our own decimal numerical system. As you
are a competent translator, you have no problem deciphering the
Babylonian writing, but you now need to write a program that
takes the sexagesimal notation and converts it to decimal.

Fortunately, each clay tablet discovered by Dr. X contains
numbers in a clean format where digits corresponding to
consecutive powers of 60 are separated by commas, with the most significant digit on the
left. For instance, one tablet contains the Babylonian number 1,24,9 in
sexagesimal, which converts to 5 049 in decimal, since 1 · 60^2 + 24 · 60^1 + 9
· 60^0 = 5 049 .

## Input
The first line contains an integer N ( 1
≤ N ≤ 20 ), the number of test cases to
follow.

Each of the following N lines represents a single tablet
containing a number in sexagesimal format. This number is a
non-empty sequence of digits separated by commas. Nonzero
digits can be any integers between 1 and 59 (inclusive), and 0 is represented by an empty string.
The sexagesimal number does not begin with a comma, contains at
least one nonzero digit, and consists of D digits in total, where 1 ≤ D ≤ 8 .

## Output
For each test case, output a line containing the decimal
representation of the sexagesimal number.

### Sample 1
**Input**
```text
3
40
1,24,9
1,,,
```
**Output**
```text
40
5049
216000
```
