A positive integer p is called a perfect number if all the
proper divisors of p sum
to p exactly. Integer d is a proper divisor of p if 1 ≤ d ≤ p-1 and p is evenly divisible by d . For example, the
number 28 is a perfect
number, since its proper divisors (which are 1 , 2 , 4 , 7 and 14 ) add up to 28 .

Perfect numbers are rare; only 50 of them are known (as of 2017).
Perhaps the definition of perfection is a little too strict.
Instead, we will consider numbers that we’ll call almost perfect . Positive integer p is almost perfect if the proper
divisors of p sum to a
value that differs from p by no more than two.

## Input
Input consists of a sequence of up to 500 integers, one per line. Each
integer is in the range 2 to 10^9 (inclusive). Input ends at end
of file.

## Output
For each input value, output the same value and then one of
the following: “perfect” (if the number is perfect), “almost
perfect” (if it is almost perfect but not perfect), or “not
perfect” (otherwise).

### Sample 1
**Input**
```text
6
65
650
```
**Output**
```text
6 perfect
65 not perfect
650 almost perfect
```
