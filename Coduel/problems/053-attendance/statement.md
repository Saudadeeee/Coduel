Taking attendance in your class is a tedious task. You call
out the names of students one at a time in alphabetical order.
If the student is present, they respond by saying “ Present! ” before you call the next name.

This is such a boring task that you sometimes zone out and
don’t keep a proper record of attendance. Write a program to
help you summarize the absences!

## Input
The first line of input contains a single integer N (1 ≤ N ≤ 200) indicating the
number of “callouts”. Then N lines follow indicating the
callouts that were made in the order they were made. A single
line consists of either a student’s name or of the response Present! . A student’s name will
consist of between 2 and 10 characters, the first
always being an uppercase letter ( ’A’ - ’Z’ ) and the
remaining characters always being lowercase letters ( ’a’ - ’z’ ).

The student names will appear in alphabetical order in this
input and a line with the response Present! will only appear if the previous line
was the name of a student. In particular, the response Present! will never appear as the
first callout.

## Output
Output the names of all students that are absent in the
order they were called, each on a separate line. If no students
were absent, simply output the message No
Absences

### Sample 1
**Input**
```text
6
Buckley
Burnadette
Present!
Chad
Present!
Erin
```
**Output**
```text
Buckley
Erin
```

### Sample 2
**Input**
```text
3
Alice
Bob
Charlie
```
**Output**
```text
Alice
Bob
Charlie
```

### Sample 3
**Input**
```text
8
Gregory
Present!
Maureen
Present!
Milton
Present!
Xavier
Present!
```
**Output**
```text
No Absences
```

### Sample 4
**Input**
```text
5
Gift
Present!
Present
Treat
Present!
```
**Output**
```text
Present
```
