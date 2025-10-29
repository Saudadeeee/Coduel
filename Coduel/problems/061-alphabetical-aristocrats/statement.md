![/problems/alphabeticalaristocrats/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/alphabeticalaristocrats/file/statement/en/img-0001.jpg)
Tavern Scene by Abraham van den Hecken the Younger. CC0 on Wikimedia Commons

It is the year 1830 of our Lord, 15 years after the Kingdom
of the Netherlands gained independence from its French
oppressors. You are secretary of state and aide to his highness
William I, Grand Duke of Luxembourg and King of the Netherlands
– an empire that is destined to prosper and stretch across
centuries to come. To the King’s utter dismay, rogue scoundrels
from the south recently dared to defy his benevolent rule. They
call themselves Belgians and declared their own kingdom – a
fact that his highness will surely deny for at least another
seven to eleven years. King William, in all his wisdom, decided
to call upon the most trusted noblemen to scheme a campaign
against the insubordinate elements that will last more than
nine days.

You are to assemble a list of trustworthy royalty and sort
them according to the Dutch rules. The Dutch rules state that
surnames are to be compared lexicographically, according to the
values of the ASCII characters, and considering only the part
starting from the first capital letter. For example, King
William compares the surname of his favourite painter Abraham van den Hecken the Younger according
to Hecken the Younger .

## Input
The input consists of:

- One line with an integer n ( 1≤ n≤ 1000 ), the number of
surnames.
- n lines, each
with a string s ( 1≤ |s|≤ 50 ),
one of the surnames. The surnames consist of English letters, spaces, and
apostrophes ( A-Z , a-z , ‘ ’, ‘ ' ’).

It is guaranteed that the part starting with the first
capital letter is unique. Names have no leading, trailing, or
consecutive spaces.

## Output
Output the list of surnames, sorted according to the Dutch
rules.

### Sample 1
**Input**
```text
7
van der Steen
fakederSteenOfficial
Groot Koerkamp
Bakker
van den Hecken the Younger
de Waal
van 't Hek
```
**Output**
```text
Bakker
Groot Koerkamp
van den Hecken the Younger
van 't Hek
van der Steen
fakederSteenOfficial
de Waal
```

### Sample 2
**Input**
```text
5
var Emreis
an Gleanna
Terzieff Godefroy
aep Ceallach
of Rivia
```
**Output**
```text
aep Ceallach
var Emreis
an Gleanna
of Rivia
Terzieff Godefroy
```

### Sample 3
**Input**
```text
7
van den Brand
den Brand Heek
Brand 'Heek
van Brand heek
DeN bRAnD hEeK
den brandHeek
der Brandheek
```
**Output**
```text
van den Brand
Brand 'Heek
den Brand Heek
van Brand heek
der Brandheek
DeN bRAnD hEeK
den brandHeek
```
