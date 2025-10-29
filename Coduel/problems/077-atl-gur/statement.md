Guðmundur is a Ph.D. student at an Icelandic university,
where he studies history. He has a burning interest in duels
and the ways of knights of past times. In the middle ages, and
the ages before them, battles between knights were common. His
research revolves around these knights and, in particular, he
is interested in writing about the most victorious knight.

Guðmundur has found a manuscript describing n knights. In the manuscript, the
knights had been ordered by their tendency towards violence.
The first knight would therefore challenge the second knight to
a battle. The winner of the battle would then challenge the
third knight, and so forth. At all moments, there was only one
active battle and only two knights participated in each
battle.

The knight that made the challenge struck first. When knight i struck another knight j , he reduced the health
of the other knight, h_
j , by the value of his strength s_ i . If the health of the other
knight, h_ j , was no
longer a positive number, then knight j had lost and knight i stood victorious. Otherwise, the
battle continued and the other knight struck next. The battle
continued until one of the knights was victorious, and that
knight would continue on to the next battle. All the damage
that was done to the knights was permanent, they did not
recover between battles.

There can be only one that stands victorious after all the
battles. Which knight will win?

## Input
The first line of the input contains one integer n , the number of
knights, where 1 ≤ n ≤ 1 
000 . Then n lines follow, the i th of
which consists of two integers h_ i , the health of knight i , and s_ i , the strength of knight i , where 1 ≤ h_ i, s_ i, ≤ 10 
000 .

## Output
Output one integer, the index of the knight that stands
victorious after all the battles.

### Sample 1
**Input**
```text
3
4 1
4 1
2 1
```
**Output**
```text
3
```

### Sample 2
**Input**
```text
6
12 1
4 3
2 6
3 4
1 12
6 2
```
**Output**
```text
3
```

### Sample 3
**Input**
```text
5
14 3
43 6
32 8
13 9
29 5
```
**Output**
```text
5
```
