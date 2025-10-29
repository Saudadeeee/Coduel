![/problems/beekeeper/file/statement/en/img-0001.png](https://open.kattis.com/problems/beekeeper/file/statement/en/img-0001.png)

It’s Bill the beekeeper again. In this problem, we learn
that didn’t choose his career for the best reason. Bill chose
to be a beekeeper because he really, really likes the look of
the double e’s in the word “beekeeper”. Your task is to help
identify other words Bill will really like.

Bill’s affinity for a word is determined by how many pairs
of double vowels it has, where vowels are the letters
a,e,i,o,u,y. Given a list of words, find the word that has
the most pairs of double vowels, as it will be Bill’s favorite
word.

Notes:

- It is guaranteed that there will be a unique correct
answer. That is, one word in the list will have strictly
more pairs of vowels than all other words in the list.
- No word in the input will have three or more of the same
vowel consecutively, because that would just be too much
for poor Bill.

## Input
The input will contain multiple test cases, up to 10 . The first line of
each case contains N ,
the number of words in that case ( 0 < N ≤ 1000 ). The next N lines will contain the
words that make up that case. Each word will contain only
lowercase English letters [a-z] , and
no word will be longer than 80 characters. Words will not
necessarily be actual English words, but they will contain at
least one letter. The input will be terminated by a line
containing a single zero.

## Output
For each case, print Bill’s favorite word. Each output
should be printed on its own line.

### Sample 1
**Input**
```text
4
artist
engineer
beekeeper
programmer
3
bookkatt
jailaikia
yeehaaw
0
```
**Output**
```text
beekeeper
yeehaaw
```
