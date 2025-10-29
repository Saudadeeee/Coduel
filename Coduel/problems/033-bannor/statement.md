![/problems/bannord/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/bannord/file/statement/en/img-0001.jpg)
Text by Michael Dziedzic, Unsplash

The office life is a blast, constant excitement and never
a frown in sight. But this lasseiz-faire attitude leads to
carelessness. A recent example of this is when you asked your
receptionist to write a memo but, in a bout of enjoyment, he
forgot the only (and therefore most important) rule in the
office: No memo should include

. The
forbidden letters are decided each week by the management, and
a word that contains a forbidden letter is a

. Worst of all, it is

pm on a Friday. Is there any way
to quickly black out the forbidden words?

## Input
The first line of the input contains a non-empty string S . The string S contains lower case
letters of the English alphabet and none of which is repeated.
The next line of the input contains the string M . The string M contains only lower case letters
and spaces and is not longer than 10^5 characters. There are no
adjacent spaces in M .
The string S corresponds
to this weeks forbidden letters and the string M corresponds to the memo.

## Output
The only line of the output should contain the memo, but
every letter in every forbidden word should be replaced by
,, * ”.

## Scoring
### Sample 1
**Input**
```text
e
we need to improve synergy through team building exercises
```
**Output**
```text
** **** to ******* ******* through **** building *********
```

### Sample 2
**Input**
```text
kmzy
krummi svaf i klettagja kaldri vetrar nottu a verdur margt ad meini verdur margt ad meini
```
**Output**
```text
****** svaf i ********* ****** vetrar nottu a verdur ***** ad ***** verdur ***** ad *****
```
