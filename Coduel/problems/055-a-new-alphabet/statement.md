![/problems/anewalphabet/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/anewalphabet/file/statement/en/img-0001.jpg)
Photo by r.
nial bradshaw

A New Alphabet has been developed for Internet
communications. While the glyphs of the new alphabet don’t
necessarily improve communications in any meaningful way, they
certainly make us feel cooler .

You are tasked with creating a translation program to speed
up the switch to our more elite New Alphabet by
automatically translating ASCII plaintext symbols to our new
symbol set.

The new alphabet is a one-to-many translation (one character
of the English alphabet translates to anywhere between 1 and 6 other characters), with each
character translation as follows:

For instance, translating the string “Hello World!” would
result in:

Note that uppercase and lowercase letters are both
converted, and any other characters remain the same (the
exclamation point and space in this example).

## Input
Input contains one line of text, terminated by a newline.
The text may contain any characters in the ASCII range 32 – 126 (space through tilde), as well
as 9 (tab). Only
characters listed in the above table (A–Z, a–z) should be
translated; any non-alphabet characters should be printed (and
not modified). Input has at most 10 000 characters.

## Output
Output the input text with each letter (lowercase and
uppercase) translated into its New Alphabet counterpart.

### Sample 1
**Input**
```text
All your base are belong to us.
```
**Output**
```text
@11 `/0|_||Z 8@$3 @|Z3 8310[]\[]6 ']['0 |_|$.
```

### Sample 2
**Input**
```text
What's the Frequency, Kenneth?
```
**Output**
```text
\/\/[-]@'][''$ ']['[-]3 #|Z3(,)|_|3[]\[](`/, |<3[]\[][]\[]3']['[-]?
```

### Sample 3
**Input**
```text
A new alphabet!
```
**Output**
```text
@ []\[]3\/\/ @1|D[-]@83']['!
```
