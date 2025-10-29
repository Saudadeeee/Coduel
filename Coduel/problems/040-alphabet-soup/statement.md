![/problems/alphabetsoup/file/statement/en/img-0001.jpeg](https://open.kattis.com/problems/alphabetsoup/file/statement/en/img-0001.jpeg)
Photo by Scott Veg. Retrieved from flickr.com. CC BY
2.0 . Source

Andrew is making himself a nice warm bowl of alphabet soup.
However, before Andrew can eat the soup, he needs to make sure
that it contains every letter of the alphabet. Can you write an
algorithm that will tell him if his soup has all of the letters
in it, and if not, which letters are missing?

## Input
Input is a single line of uppercase letters (A-Z) of length L ( 0 <= L <= 1 000 000 ),
possibly containing duplicates.

## Output
If all letters A-Z are present in the input, the output
should be “ Alphabet Soup! ”.
Otherwise, the output should be a single line containing all of
the uppercase letters that were missing from the input string,
in alphabetical order.

### Sample 1
**Input**
```text
AQUICKBROWNFOXJUMPSOVERTHELAZYDOG
```
**Output**
```text
Alphabet Soup!
```

### Sample 2
**Input**
```text
QWBGHMJKLXYCDRSZTVNPF
```
**Output**
```text
AEIOU
```
