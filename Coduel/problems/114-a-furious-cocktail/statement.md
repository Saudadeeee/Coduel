![/problems/cocktail/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/cocktail/file/statement/en/img-0001.jpg)
Getting the “A Furious Cocktail” advancement

In Minecraft, potions can be made and drank. When drank,
they apply the corresponding potion effect to the player for
some specified amount of time. “A Furious Cocktail” is the name
of the advancement where a player has every potion effect
applied at the same time. This is a challenging feat, as it
takes time to drink each potion, and only one potion can be
drank at a time.

Suppose that in your inventory, there are N unique potions that have a time
duration of t_1, … , t_
N seconds, respectively. Assuming that it takes T seconds to drink a
potion, is it possible to have all N potion effects applied at the same
time? Note that if one potion’s effect ends at the same time
you finish drinking another potion, the potions are not
considered to be applied at the same time.

## Input
The first line consists of 2 integers, 0 < N < 1 000 and 1 ≤ T ≤ 10 , the
number of potions in your inventory and time in seconds it
takes to drink each potion, respectively. The next N lines each consists of an integer 1 ≤ t_ i ≤ 10^6 ,
the time duration of the i -th potion where i ranges from 1 to N .

## Output
Output “YES” if it is possible to have all N potion effects applied at the same
time, “NO” if otherwise.

### Sample 1
**Input**
```text
5 1
1
2
3
4
5
```
**Output**
```text
YES
```

### Sample 2
**Input**
```text
3 2
4
3
2
```
**Output**
```text
NO
```

### Sample 3
**Input**
```text
3 2
2
3
5
```
**Output**
```text
YES
```
