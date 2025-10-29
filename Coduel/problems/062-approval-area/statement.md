The current policy of the government can be represented by a
point in the plane. A voter’s ideal policy would also be
represented by a point in the plane. The voter’s unhappiness
with the current policy is measured by the distance between
these two points. Many different distance metrics may be used,
but we will use squared Euclidean distance here.

The voter’s unhappiness with the current policy is u . A new policy is
proposed and is put to the vote.

The voter’s approval area is the set of points representing
policies that the voter would be willing to vote for to replace
the current policy. Determine the area of the voter’s approval
area.

## Input
The first and only line contains one integer u , where 0 ≤ u ≤ 4 · 10^14 .

## Output
Output the area of the voter’s approval area. Your output is
considered correct if it has at most a relative error of 10^-9 .

### Sample 1
**Input**
```text
0
```
**Output**
```text
0E-100
```

### Sample 2
**Input**
```text
3
```
**Output**
```text
9.424777960769379715387930149838508652591508198125317462924833776923449218858626995884104476026351204
```

### Sample 3
**Input**
```text
400000000000000
```
**Output**
```text
1256637061435917.295385057353311801153678867759750042328389977836923126562514483599451213930136846827
```
