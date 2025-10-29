Many magnificent minstrels have made massive manuscripts
made with multitudes of matching marks. Indeed, introverted
intellectuals not infrequently instigate these intriguing
itineraries intending to invigorate their insatiable
intellects. Nevertheless…you get the idea. For each line of
text in the input, output the letter that starts the most words
in the line. In case there’s a tie, output the first letter
alphabetically in the tie. Words in the text are always
separated by spaces or new lines; a hyphenated word only counts
as one word, not two.

## Input
The first line contains a single integer n , the number of lines of text that
follow.

The next n lines of
input are all lines of text, up to 10^6 characters long. The text
consists of only lowercase letters, spaces, and
punctuation.

## Input Restrictions
- 0 < n ≤
100

## Output
The output should be n lines long; each line of output
should only contain the letter that starts the most words in
the corresponding line of input.

### Sample 1
**Input**
```text
5
a b c a b a
t!
m z m z m z
az. bz, cz: az; bz! az?
the mitochondria is the powerhouse of the cell.
```
**Output**
```text
a
t
m
a
t
```
