![/problems/almennirborgarar/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/almennirborgarar/file/statement/en/img-0001.jpg)
Image from Unsplash

For years contestants in Forritunarkeppni
Framhaldsskólanna have gotten delicious hamburgers from
Hamborgarabúlla Tómasar for lunch. The contestants form an
orderly line where they wait while the chefs are hard at work
at the grills. Búllan’s chefs are very talented. They are so
talented that they assemble the burger instantly. The only
thing that takes time is the grilling process. Búllan has

small grills (numbered
from

to

) and each grill can grill one
burger at a time. The grills also work at different
temperatures, so they don’t take the same time to grill a
burger. The chefs have measured that grill

takes

seconds to grill a single
burger.

Benni, an ardent competitive programmer (and hamburger
enthusiast), is waiting in line with m other contestants in front of him.
How long will Benni have to wait if the chefs utilize the
grills optimally?

## Input
The first line of the input contains two integers n ( 1 ≤ n ≤ 2· 10^5 ), the
number of grills, and m ( 0 ≤ m ≤ 10^9 ),
the number of contestants ahead of Benni in line.

Then there is a line with n integers, t_1, t_2, … , t_ n , where t_ i ( 1 ≤ t_ i ≤ 10^9 ) is the number
of seconds it takes the i -th grill to grill a burger.

## Output
Print the number of seconds Benni has to wait before he gets
his burger, assuming the chefs utilize the grills
optimally.

## Scoring
### Sample 1
**Input**
```text
2 6
1 2
```
**Output**
```text
5
```

### Sample 2
**Input**
```text
3 10
2 7 5
```
**Output**
```text
14
```

### Sample 3
**Input**
```text
4 6
10 120 25 30
```
**Output**
```text
50
```
