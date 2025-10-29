![/problems/99problems/file/statement/en/img-0001.png](https://open.kattis.com/problems/99problems/file/statement/en/img-0001.png)

Ingrid is the founder of a company that sells bicycle parts.
She used to set the prices of products quite arbitrarily, but
now she has decided that it would be more profitable if the
prices end in 99 .

You are given a positive integer N , the price of a product. Your task
is to find the nearest positive integer to N which ends in 99 . If there are two such numbers
that are equally close, find the bigger one.

## Input
The input contains one integer N ( 1
≤ N ≤ 10^4 ), the price of a product. It is
guaranteed that the number N does not end in 99 .

## Output
Print one integer, the closest positive integer that ends in 99 . In case of a tie,
print the bigger one.

### Sample 1
**Input**
```text
10
```
**Output**
```text
99
```

### Sample 2
**Input**
```text
249
```
**Output**
```text
299
```

### Sample 3
**Input**
```text
10000
```
**Output**
```text
9999
```
