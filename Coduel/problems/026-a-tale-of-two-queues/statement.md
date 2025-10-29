![/problems/ataleoftwoqueues/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/ataleoftwoqueues/file/statement/en/img-0001.jpg)
The two queues.

Following yet another all-nighter of studying patterns in
permutations at the university, Unnar is both exhausted and
starving. Fortunately it is almost noon, and the cafeteria has
started serving lunch.

After heading downstairs, Unnar is sad to see that the
cafeteria is already full of hungry students, and that the two
queues towards the two registers are already quite long.
Although he would prefer shorter queues, years of eating at the
cafeteria has made Unnar an expert at estimating how long
different individuals take to pay for their food at the
register.

The methods Unnar uses to perform these very accurate
estimations require years of training to even begin to
understand, but they are based on observations such as whether
the individual has their credit card or cash ready, the amount
and cost of the items they intend to purchase, and whether they
are staff members.

After making his complex estimations for each individual in
each queue, Unnar would like to know which queue he should
enter in order to get to the register as quickly as possible,
assuming his estimations are correct (which they always are!).
At this point his sleep deprivation is really starting to kick
in, and he asks you to help him with this final task.

## Input
The input consists of:

- One line with two integers n and m ( 1 ≤ n,m ≤ 5 000 ), the
number of individuals in the left and right queues.
- One line with n integers, the i th of
which represents the estimated time, in seconds, for the i th individual in
the left queue.
- One line with m integers, the i th of
which represents the estimated time, in seconds, for the i th individual in
the right queue.

Individuals are listed in their queue order, with the next
in queue being listed first.

## Output
If it is quicker for Unnar to enter the left queue, output
“ left ”. If it is quicker for Unnar to
enter the right queue, output “ right ”. If it does not matter which queue Unnar
enters, output “ either ”.

### Sample 1
**Input**
```text
4 2
10 9 8 15
32 40
```
**Output**
```text
left
```

### Sample 2
**Input**
```text
2 3
15 15
10 10 10
```
**Output**
```text
either
```

### Sample 3
**Input**
```text
4 1
20 20 20 20
60
```
**Output**
```text
right
```
