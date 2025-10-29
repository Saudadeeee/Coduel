![/problems/battleofnieuwpoort/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/battleofnieuwpoort/file/statement/en/img-0001.jpg)
Prince Maurice at the Battle of Nieuwpoort, 2 July
1600 , Pauwels van Hillegaert (1596–1640),
Oil on panel, circa 1632–1640. Public domain,
Rijksmuseum Amsterdam and Wikimedia Commons

The battle of Nieuwpoort occurred in the
year 1600 . This is
famously easy to remember, because it ends in two zeros. Alas,
not all historical events have been so obliging!

You suspect that the problem is with the fixation of
historians on the decimal system. Maybe, given the year of
another battle, there exists a small base (at most 16 ) in which this year would also be
easy to remember?

## Input
The input consists of:

- One line with 4 tokens: One integer y ( 1≤ y≤
2024 , in base- 10 ), the year of the
battle. Three words w ( 2≤ |w|≤
20 ), naming the battle. The words only consist of English letters ( A-Z and a-z ).

## Output
If it is possible to rewrite the year to make it easier to
remember, output this base b ( 2≤ b≤
16 , in base- 10 ) and the year written in
base- b . Otherwise,
output “ impossible ”.

The year in base- b must end with “ 00 ” and must not start
with ‘ 0 ’.

Use letters ‘ a ’, ‘ b ’, ‘ c ’, etc. for the
digits following ‘ 9 ’ in bases higher
than 10 .

If there are multiple valid solutions, you may output any
one of them.

### Sample 1
**Input**
```text
1600 Battle of Nieuwpoort
```
**Output**
```text
10 1600
```

### Sample 2
**Input**
```text
625 Battle of Sarus
```
**Output**
```text
5 10000
```

### Sample 3
**Input**
```text
1600 Battle of Sekigahara
```
**Output**
```text
8 3100
```

### Sample 4
**Input**
```text
1815 Battle of Waterloo
```
**Output**
```text
11 1400
```

### Sample 5
**Input**
```text
1859 Battle of Solferino
```
**Output**
```text
13 b00
```

### Sample 6
**Input**
```text
1848 Battle of Bov
```
**Output**
```text
2 11100111000
```

### Sample 7
**Input**
```text
1453 Fall of Constantinople
```
**Output**
```text
impossible
```
