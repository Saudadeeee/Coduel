![/problems/artichoke/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/artichoke/file/statement/en/img-0001.jpg)
Picture by Hans Hillewaert via Wikimedia Commons

Fatima Cynara is an analyst at Amalgamated Artichokes
(AA). As with any company, AA has had some very good times as
well as some bad ones. Fatima does trending analysis of the
stock prices for AA, and she wants to determine the largest
decline in stock prices over various time spans. For example,
if over a span of time the stock prices were

,

,

,

,

and

, then the largest decline would
be

between the first
and fourth price. If the last price had been

instead of

, then the largest decline would
have been

between the
last two prices.

Fatima has done some previous analyses and has found that
the stock price over any period of time can be modelled
reasonably accurately with the following
equation:

where p , a , b , c and d are constants. Fatima would like
you to write a program to determine the largest price decline
over a given sequence of prices. Figure 1 illustrates the
price function for Sample Input 1. You have to consider
the prices only for integer values of k .

## Input
The input consists of a single line containing 6 integers p ( 1
≤ p ≤ 1 000 ), a , b , c , d ( 0
≤ a, b, c, d ≤ 1 000 ) and n ( 1
≤ n ≤ 10^6 ). The first 5 integers are described above. The
sequence of stock prices to consider is operatorname price(1), operatorname
price(2), … , operatorname price(n) .

## Output
Display the maximum decline in the stock prices. If there is
no decline, display the number 0 . Your output should have an
absolute or relative error of at most 10^-6 .

### Sample 1
**Input**
```text
42 1 23 4 8 10
```
**Output**
```text
104.855110477
```

### Sample 2
**Input**
```text
100 7 615 998 801 3
```
**Output**
```text
0.00
```

### Sample 3
**Input**
```text
100 432 406 867 60 1000
```
**Output**
```text
399.303813
```
