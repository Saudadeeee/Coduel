Due to the empire’s strict control over the galaxy, one of
the Rebels droids, A-P5, started to encrypt the distance of
hyperspace jumps so that the empire is unable to track the
rebel fleet. You are currently being followed by the empire and
must calculate the jump to hyperspace. Your incompetent droid
co-pilot failed to download the correct decryption program back
on the base. Thus, in order to get the proper hyperspace
coordinates, you must write a program to decrypt the hyperspace
distance you will travel.

Decryption involves two numbers. The first number will be
the decryption key, and the second is the number to decrypt. In
order to decrypt the number, you must take the key and add it
to each digit of the encrypted number. Any carried digits
should be removed.

## Input
The first line of input consists of a single integer t ( 1 ≤ t < 100 ), which indicates
the number of test cases that follow.

Each test case consists of a single line containing two
integers: k ( 0 ≤ k ≤ 9 ), which
indicates the encryption key, and n ( 1
≤ n < 2^31 ), which indicates the encrypted
number. n will never
have any leading zeroes.

## Output
For each test case, output the decrypted number on its own
line. Be sure to include leading zeroes in
your output as necessary so that the output has the same number
of digits as n .

### Sample 1
**Input**
```text
3
1 12345
5 98765
9 55555
```
**Output**
```text
23456
43210
44444
```
