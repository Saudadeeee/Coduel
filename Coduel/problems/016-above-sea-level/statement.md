![/problems/abovesealevel/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/abovesealevel/file/statement/en/img-0001.jpg)
Photo by L.W. on Unsplash

As a GPS hobbyist, you are interested in looking at how a
database of altitude recordings will change to account for sea
level rise. For your projections, you will assume that between
now and 2050 , the sea
level will rise by 30 centimeters. Your input will be a single altitude entry from a
database of geolocations (given in meters). You need to output
what that altitude will be in 2050 , modified by your sea level
rise projection.

## Input
A single real number -100 
000 ≤ N ≤ 100 000 , representing a single
altitude entry. The number contains at most 4 digits after the decimal
point.

## Output
Print the predicted altitude in 2050 . Your output must be within 0.001 of the correct
answer to be accepted.

### Sample 1
**Input**
```text
150.5
```
**Output**
```text
150.2
```

### Sample 2
**Input**
```text
60580.6373
```
**Output**
```text
60580.3373
```

### Sample 3
**Input**
```text
-475.1901
```
**Output**
```text
-475.4901
```
