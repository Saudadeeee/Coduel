![/problems/arithmeticadaptation/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/arithmeticadaptation/file/statement/en/img-0001.jpg)
Postcard showing a Norwegian by solving Sample 3.
Coloured black and white photo, National Library of Norway.

Practice does make perfect! You have finally achieved
proficiency at the task of adding two small nonzero
integers a and b to compute
their sum a+b .
Before you move on to studying four-digit numbers, you want to
achieve mastery by also understanding the inverse problem:
given integer s ,
determine nonzero a and b such that a+b=s . None of the numbers may use
more than 3 digits.

## Input
The input consists of:

- One line with an integer s such that -999≤ s≤ 999 .

## Output
Output two integers a (with -999≤ a≤ 999 and a≠ 0 ) and b (with -999≤ b≤ 999 and b≠ 0 ) such that a+b=s . If there is more than one
valid solution, you may output any one of them.

## Explanation of Sample Input 1
On input “ 10 ”, the output
“ 3 7 ” is correct because 3+7=10 . Note that many other outputs
would also be correct, such as “ 2 8 ”,
“ 11 -1 ”, or even “ -849 859 ”. On the other hand, the answer
“ 4 7 ” would be wrong (because 4+7≠ 10 ),
and so would “ 10 0 ” (because both a and b must be nonzero) and “ 1000 -990 ” (because both a and b must have at most three
digits.)

### Sample 1
**Input**
```text
10
```
**Output**
```text
3 7
```

### Sample 2
**Input**
```text
-1
```
**Output**
```text
-2 1
```

### Sample 3
**Input**
```text
3
```
**Output**
```text
1 2
```

### Sample 4
**Input**
```text
0
```
**Output**
```text
-999 999
```
