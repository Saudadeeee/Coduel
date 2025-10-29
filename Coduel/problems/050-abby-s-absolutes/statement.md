![/problems/abbysabsolutes/file/statement/en/img-0001.jpg](https://open.kattis.com/problems/abbysabsolutes/file/statement/en/img-0001.jpg)
Photo by gibblesmash asdf on Unsplash

Abby has offered to buy you some apples. However, she is
very absolute about things.

You may ask her to buy a certain number of apples, but she
may buy more apples if she figures that you want a lot of
apples, or just buy one apple if she figures that you do not
want very many apples. So, if the number of apples you want is
closer to Abby’s upper threshold than it is to 1 , then she will buy a number of
apples equal to her upper threshold. Otherwise, she will just
buy one apple. If it is equally close to 1 and her upper threshold, she will
just buy 1 apple.

You want to figure out the total number of apples Abby will
buy for you after she takes one or more trips to the grocery
store.

## Input
The input will consist of two lines.

The first line will contain two space-separated integers.
The first integer 1 ≤ N ≤
10 000 is the number of apples Abby will buy if she
is buying a lot of apples. The second integer 1 ≤ K ≤ 100 is the number of
trips to the store Abby will take.

The second line will contain K space-separated integers
representing the number of apples you want to buy on each of
Abby’s trips to the store, with each of these integers being
between 1 and N , inclusive.

## Output
Output K space-separated integers representing the number of apples Abby
will buy for you for each of her trips to the store.

### Sample 1
**Input**
```text
5 5
1 2 3 4 5
```
**Output**
```text
1 1 1 5 5
```

### Sample 2
**Input**
```text
6 8
1 5 4 2 5 4 6 4
```
**Output**
```text
1 6 6 1 6 6 6 6
```
