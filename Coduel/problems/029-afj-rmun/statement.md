![/problems/afjormun/file/statement/en/img-0001.png](https://open.kattis.com/problems/afjormun/file/statement/en/img-0001.png)
Svampur Sveinsson (Image from deviantart.com )

Undoubtedly you have notices these so called “memes’
which have been popping up on the internet these past few
years. One of these memes is known as the “Spongebob meme”,
where a sarcastic text is written on an image of Spongebob
Squarepants. The interesting thing about these memes is the
text is written in alternating uppercase and lowercase
characters. Your task is to alter the “Spongebob-memed” string
to a form where the first characer of each sentence is an
uppercase character, but the other characters are lowercase.
This is operation is “unmemeing“ a string. An example of a
“Spongebob memed” string is the text “FoRrItUn Er SkEmMtIlEg.”,
whereas the unmemed version of the text is “Forritun er
skemmtileg.”

## Input
The first line will contain the integer n ( 1
≤ n ≤ 10^4 ), the number of sentences in the memed
text. The following n lines will include one memed sentence each. Each sentence is at
most 300 characters.

Note that a sentence always ends with a full stop and the
first character of each sentence can either be lowercase or
uppercase. Also note that all characters are in the English
alphabet.

## Output
Write the sentences which appear in the input, in the same
order, except each sentence should be written in unmemed
form.

## Scoring
### Sample 1
**Input**
```text
1
FoRrItUn Er SkEmMtIlEg.
```
**Output**
```text
Forritun er skemmtileg.
```

### Sample 2
**Input**
```text
2
tHe MiToChOnDrIa Is ThE pOwErHoUsE oF tHe CeLl.
MeMeS aRe FuN.
```
**Output**
```text
The mitochondria is the powerhouse of the cell.
Memes are fun.
```
