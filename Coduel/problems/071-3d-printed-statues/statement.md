![/problems/3dprinter/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/3dprinter/file/statement/en/img-0001.jpg)
Picture by
Ariosvaldo Gonzáfoles, cc-by

You have a single 3D printer, and would like to use it to
produce n statues.
However, printing the statues one by one on the 3D printer
takes a long time, so it may be more time-efficient to first
use the 3D printer to print a new printer. That new printer may
then in turn be used to print statues or even more printers.
Print jobs take a full day, and every day you can choose for
each printer in your possession to have it print a statue, or
to have it 3D print a new printer (which becomes available for
use the next day).

What is the minimum possible number of days needed to print
at least n statues?

## Input
The input contains a single integer n ( 1
≤ n ≤ 10 000 ), the number of statues you need to
print.

## Output
Output a single integer, the minimum number of days needed
to print at least n statues.

### Sample 1
**Input**
```text
1
```
**Output**
```text
1
```

### Sample 2
**Input**
```text
5
```
**Output**
```text
4
```
