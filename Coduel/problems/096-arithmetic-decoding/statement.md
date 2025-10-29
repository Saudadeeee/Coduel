Arithmetic coding is a method to represent a message as a
real number x such that 0 ≤ x < 1 . We will
assume that the message consists only of uppercase ‘A’s and
‘B’s. The two letters have associated probabilities p_ A and p_ B = 1 - p_ A such that 0 < p_ A < 1 .

The current interval [a,b) is initially set to [0,1) and we will update
this interval one letter at a time. To encode a letter, the
current interval is divided into two subintervals as follows.
Let c = a + p_ A(b-a) .
If the next letter is ‘A’, [a,c) becomes the current interval.
Otherwise, the current interval is now [c,b) . This process is repeated for
each letter in the message. If [k,ell ) is the final interval, the
encoded message is chosen to be k .

For example, if the original message is “ABAB” and p_ A = p_ B = 0.5 , the
sequence of intervals encountered in the algorithm
is

The encoded message is therefore 0.3125, or 0.0101 in
binary.

Given the length of the message, the probabilities, and the
encoded message, determine the original message.

## Input
The first line contains the integer N ( 1
≤ N ≤ 15 ), which is the length of the original
message. The second line contains the integer D ( 1
≤ D ≤ 7 ), which indicates that p_ A = fracD8 . The third line
contains the binary representation of the encoded message. It
is guaranteed that the binary representation of the encoded
message starts with “0.” and contains at most 3N+2 characters.

It is guaranteed that the encoded message came from an
initial message of length N consisting only of ‘A’ and ‘B’
using this value of p_
A .

## Output
Display the original message.

### Sample 1
**Input**
```text
4
4
0.0101
```
**Output**
```text
ABAB
```

### Sample 2
**Input**
```text
6
5
0.100100100100101
```
**Output**
```text
ABBABA
```
