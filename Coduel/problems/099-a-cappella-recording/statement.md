Geoffry is preparing an a cappella composition where he
sings the entire song by himself.

Each note of the song has a pitch between 0 and 10^9 . Because of the varying pitches
in the song, Geoffry will record himself singing multiple
times. In a single recording, he will pick some subset of the
notes to sing and he will sing exactly those notes. To avoid
straining his voice too much, within a single recording, there
is a limit to the difference between the maximum pitch and the
minimum pitch among the notes he sings.

Compute the minimum number of times that Geoffry can record
himself singing the song and each note is sung in at least one
of the recordings.

## Input
The first line contains two integers n and d ( 1
≤ n ≤ 10^5, 0 ≤ d ≤ 10^9 ), where n is the number of notes in
Geoffry’s song, and d is
the largest difference between the minimum pitch and the
maximum pitch that Geoffry can handle.

Each of the next n lines contains a single integer p ( 0
≤ p ≤ 10^9 ). These are the pitches of the notes in
Geoffry’s song, in the order that they are to be sung.

## Output
Output a single integer, which is the minimum number of
times that Geoffry can record himself singing the song and each
note is sung in at least one of the recordings.

### Sample 1
**Input**
```text
6 0
3
1
4
1
5
9
```
**Output**
```text
5
```

### Sample 2
**Input**
```text
6 1
3
1
4
1
5
9
```
**Output**
```text
4
```

### Sample 3
**Input**
```text
6 2
3
1
4
1
5
9
```
**Output**
```text
3
```

### Sample 4
**Input**
```text
6 4
3
1
4
1
5
9
```
**Output**
```text
2
```

### Sample 5
**Input**
```text
6 8
3
1
4
1
5
9
```
**Output**
```text
1
```
