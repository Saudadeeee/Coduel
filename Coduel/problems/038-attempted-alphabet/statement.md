![/problems/attemptedalphabet/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/attemptedalphabet/file/statement/en/img-0001.jpg)
Photo of fridge magnets by lylamerle . CC-BY-2.0.

Your little brother Al is learning to say the alphabet, but
he is not very good at it yet. In particular, he often forgets
some of the letters. When he’s practicing by himself it’s hard
for him to tell whether he’s forgotten any letters, so he asks
for your help. Your job is to listen to him recite the
alphabet, and then tell him which letters he missed. This is
somewhat complicated by the fact that Al doesn’t always say the
letters in the right order; sometimes he even repeats letters
he has already said before.

## Input
The input consists of a single line of lowercase English
letters recited by Al. There is at least 1 letter and at most 52 .

## Output
Output a single line containing all the letters Al missed,
in alphabetical order. If Al didn’t miss any, then output Good job!

### Sample 1
**Input**
```text
abcdefghijklmopqrstuvwxyz
```
**Output**
```text
n
```

### Sample 2
**Input**
```text
acdefhilkgjmmmopnttavuqyz
```
**Output**
```text
brswx
```

### Sample 3
**Input**
```text
acegikmoqsuwybdfhjlnprtvxz
```
**Output**
```text
Good job!
```
