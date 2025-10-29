A prime number is an integer n ( n ≥ 2 ) such that n cannot be formed as the product of
two other integers smaller than n . In other words, a number is prime
if its factors are only one and itself. An integer which is
greater than 2 and is
not prime is called a composite
number .

An additive prime in
base- 10 is a number
which is both prime and the sum of its digits forms a
prime number. For example, 23 is an additive prime, since 23 is prime, and 2 + 3 = 5 is also prime,
but 13 is not, since 1 + 3 = 4 , and 4 is not prime.

## Input
Input consists of a single integer n ( 2
≤ n ≤ 2^31 - 1 ).

## Output
Output “ ADDITIVE PRIME ” if the
number is an additive prime. Output “ PRIME, BUT NOT ADDITIVE ” if the number is
prime, but not an additive prime. Output “ COMPOSITE ” otherwise.

### Sample 1
**Input**
```text
61
```
**Output**
```text
ADDITIVE PRIME
```

### Sample 2
**Input**
```text
17
```
**Output**
```text
PRIME, BUT NOT ADDITIVE
```

### Sample 3
**Input**
```text
141
```
**Output**
```text
COMPOSITE
```
