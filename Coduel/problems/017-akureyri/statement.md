The year 2016 is an important year for Forritunarkeppni
Framhaldsskólanna. For the first time ever the contest will be
held in two locations! But now it is the year 3016 and the
contest is held all over the country, not just in Reykjavík or
Akureyri. The contestants no longer go to the contest, the
contest comes to them. The planning committee is having some
trouble the shirt distribution as a result. There are thousands
of contestants, tens of thousands even, and the contest is too
soon for it to be possible to go over it all by hand. In the
year 3016 people are so used to computers programming for them,
aside from the occasional competitive programmer, that they
have completely forgotten how to program and have no idea how
to solve this issue.

Luckily Hjalti was cryogenically frozen in the year 2016 so
he could solve this kind of issue. Thus the committee needs
Hjalti’s help going over the list of contestants and record how
many shirts need to be sent to each location. Hjalti has been
frozen for a thousand years though and is still a bit dizzy, so
can you help him save the day?

## Input
The input starts with a single line containing a single
integer 1 ≤ N ≤ 10 
000 , denoting the number of contestants. Then there are N pairs of lines, a
total of 2N lines. Each
pair of lines contains the first name of a contestant on the
first line and their location on the second line. Both strings
only contain English lower case letters. They will contain at
least one letter and at most 100 letters.

## Output
For each location in the input, print the name of the
location and the number of contestants located there. The
locations can be printed in any order.

## Explanation of Sample Inputs
In the first sample there are two contestants in Akureyri,
Bjarki and Jonas, but Hjalti, Gunnar and Tomas are in
Reykjavík, hence the given output.

## Scoring
The solution will be tested on differently hard input data
and the data is divided into groups as shown in the table
below. The solution will then be scored according to how many
groups are solved.

### Sample 1
**Input**
```text
5
Hjalti
Reykjavik
Gunnar
Reykjavik
Bjarki
Akureyri
Tomas
Reykjavik
Jonas
Akureyri
```
**Output**
```text
Akureyri 2
Reykjavik 3
```

### Sample 2
**Input**
```text
2
Bjarki
Akureyri
Jonas
Akureyri
```
**Output**
```text
Akureyri 2
```

### Sample 3
**Input**
```text
2
Sunna
Selfoss
Saga
Akureyri
```
**Output**
```text
Akureyri 1
Selfoss 1
```
