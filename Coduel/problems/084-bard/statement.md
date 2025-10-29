Every evening villagers in a small village gather around a
big fire and sing songs.

A prominent member of the community is the bard. Every
evening, if the bard is present, he sings a brand new song that
no villager has heard before, and no other song is sung that
night. In the event that the bard is not present, other
villagers sing without him and exchange all songs that they
know.

Given the list of villagers present for E consecutive evenings, output all
villagers that know all songs sung during that period.

## Input
The first line of input contains an integer N , 2
≤ N ≤ 100 , the number of villagers. The villagers
are numbered 1 to N . Villager number 1 is the bard.

The second line contains an integer E , 1
≤ E ≤ 50 , the number of evenings.

The next E lines
contain the list of villagers present on each of the E evenings. Each line
begins with a positive integer K , 2
≤ K ≤ N , the number of villagers present that
evening, followed by K positive integers separated by spaces representing the
villagers.

No villager will appear twice in one night and the bard will
appear at least once across all nights.

## Output
Output all villagers that know all songs, including the
bard, one integer per line in ascending order.

### Sample 1
**Input**
```text
4
3
2 1 2
3 2 3 4
3 4 2 1
```
**Output**
```text
1
2
4
```

### Sample 2
**Input**
```text
8
5
4 1 3 5 6
2 5 6
3 6 7 8
2 6 2
4 2 6 8 1
```
**Output**
```text
1
2
6
8
```

### Sample 3
**Input**
```text
5
3
2 1 3
2 2 1
4 2 1 4 5
```
**Output**
```text
1
```
