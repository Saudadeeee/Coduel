![/problems/babypanda/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/babypanda/file/statement/en/img-0001.jpg)
a sneezing baby panda

Alex is taking care of a baby panda who seems to be
unusually sniffly. Every day, the baby panda may sneeze out
zero or one slime(s) into its enclosure; every night, all
slimes present in the enclosure split, so that the number of
slimes doubles overnight. Alex places the baby panda into a
clean enclosure with 0 slimes at the beginning of day 1 and observes that at the end of
night n , there are m slimes in the baby
panda’s enclosure. She is worried about the baby panda and
wants to know the number of times the baby panda sneezed out a
slime over these n days.

## Input
The only line of input contains the space-separated integers n, m ( 1 ≤ n ≤ 10^18 , 0 ≤ m ≤ 10^18 , m is even), where n is the number of days and m is the number of
slimes present after night n .

## Output
On a single line, output the number of times that the baby
panda sneezed out a slime.

### Sample 1
**Input**
```text
10 10
```
**Output**
```text
2
```

### Sample 2
**Input**
```text
10 128
```
**Output**
```text
1
```

### Sample 3
**Input**
```text
13 500
```
**Output**
```text
6
```

### Sample 4
**Input**
```text
1000000000000000000 576460752303423488
```
**Output**
```text
1
```
