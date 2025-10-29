The bank you work at had way too many customers today to
keep the queues in check, so now there are lots of people
standing in queues. In fact n people are standing around queued
up to talk to one of k tellers, so they stand in one of k separate queues.

It is time for a lunch break, so there will only be one
queue open while most of the tellers are on lunch break. To
prevent angry customers and total anarchy, you have to merge
the queues sensibly. You can ask people when they started
waiting and know they will not lie. Who would even do such a
foul thing?

The new queue should be in increasing order of arrival time,
just like the current queues are all individually in increasing
order of arrival time. Can you get this done?

You know when each person at the front of a queue arrived.
So your only operation is to pick who should join the new queue
and then ask the person behind them when they arrived.

If there is a tie between people, any way of resolving the
tie will be accepted.

## Interactivity
This is an interactive problem. Your solution will be tested
against an interactive judge which reads the output of your
solution and prints the input your solution receives. This
interaction follows certain rules:

First your program should read a line containing two
integers separated by a space, n and k . The value n denotes the number of customers
and k the number of
queues. The values satisfy n
≤ 100 000 and 2
≤ k ≤ n .

Next your program should read k integers t_1, t_2, … , t_k on a single
line separated by spaces. The value t_i denotes how many seconds after
the bank opening the person at the front of queue number i arrived. These values
are all non-negative and at most 10^9 .

Then while there are customers left to put in the new queue
the following is repeated.

Your program should print the index of the queue where you
want to let the front person join the new queue. The first
queue is index 1 and the
last index k . Then you
should read one line. If this queue is now empty this line will
say DONE . Otherwise this line will
contain a single integer T , the time the person who is now at
the front arrived. This value will be non-negative and at most 10^9 , and will also be
at least the value of the person who was at the front of the
queue before them, if any.

Once every person has joined the new queue, your program
should print DONE and then exit.

Make sure to flush after each
line, for example using

- print(..., flush=True) in Python,
- cout << ... << endl; in C++,
- System.out.flush(); in Java.

### Sample 1
