![/problems/airfaregrants/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/airfaregrants/file/statement/en/img-0001.jpg)
AI-generated image of Cupcake City.

Congratulations! Your team has advanced to the next round of
the International Cupcake Production Competition (ICPC)! To
participate in the competition, you are going to fly to Cupcake
City from your hometown. The competition organizers have just
shared good news: generous sponsors will support you with your
flight ticket!

Here’s how it works. You have already obtained a list of
available flights. Among those options, you first report the
price of any one potential flight. This determines the reimbursement limit of your trip; sponsors would pay
you up to half that price . Next, you actually purchase
your flight ticket. This flight may or may not be the same as
the flight you report for the reimbursement limit. Finally, you
show the receipt of your purchase, and sponsors will reimburse
you the minimum of your actual cost and the reimbursement
limit.

Now, you want to figure out your minimum possible net cost—the price you pay, minus the amount you get
reimbursed. Naturally, you will report the price of the most
expensive flight ticket and buy the cheapest flight ticket.

## Input
The first line of input is an integer, N ( 1
≤ N ≤ 50 ), the number of available flights.

Each of the next N lines contains an integer P ( 10
≤ P ≤ 10^5 ), which is the price of a flight
ticket from your hometown to Cupcake City, in dollars. It is
guaranteed that P is a
multiple of 10 .

## Output
Output a single integer, the minimum amount, in dollars,
that you have to pay for a flight ticket, excluding the amount
of travel support from sponsors.

### Sample 1
**Input**
```text
2
150
250
```
**Output**
```text
25
```

### Sample 2
**Input**
```text
5
200
300
150
400
500
```
**Output**
```text
0
```
