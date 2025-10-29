![/problems/backspace/file/statement/en/img-0001.png](https://open.kattis.com/problems/backspace/file/statement/en/img-0001.png)
Bjarki having problems

Right before Forritunarkeppni Framhaldsskólanna started,
Bjarki decided to update his computer. He didn’t notice
anything off until he started writing code in his favourite
editor Bim (Bjarki IMproved). Usually when he uses this editor
and presses backspace one letter to the left of the
cursor is erased. But after the update it instead writes the
letter < .
He has tried all of his editors, Bmacs, Neobim, bjedit,
NoteBjad++, Subjark Text, but they all seem to have this same
issue. He doesn’t have the time to scour the internet to find a
solution to this problem, so he decides to take matters into
his own hands and just solve this.

Help Bjarki write a program that takes as input a string he
wrote and prints the string as he intended to write it.

## Input
The first and only line of input contains a string S of length N containing only lower case English
letters and the symbol < .

## Output
Print the string as Bjarki intended to write it. That is to
say, if the string is printed letter by letter, < denotes the removal of the last printed
letter as if it were a backspace .

## Explanation of Sample Inputs
In the first sample Bjarki starts by writing a a which he then erases, then writes b and c but then
erases the c . The output is thus b . In the next sample Bjarki writes foss but then erases the last two
letters with < < , the output at this point is thus fo . He then adds to this rritun and the output is thus forritun . In the last sample he writes a and erases it immediately
afterwards twice. Then finally he writes aa and ereases it with < < .

## Scoring
The solution will be tested on differently hard input data
and the data is divided into groups as shown in the table
below. The solution will then be scored according to how many
groups are solved.

### Sample 1
**Input**
```text
a<bc<
```
**Output**
```text
b
```

### Sample 2
**Input**
```text
foss<<rritun
```
**Output**
```text
forritun
```

### Sample 3
**Input**
```text
a<a<a<aa<<
```
