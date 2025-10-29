![/problems/bendilfaerslur/file/statement/en/img-0001.png](https://open.kattis.com/problems/bendilfaerslur/file/statement/en/img-0001.png)
Image from RIPE NCC

Níels is very forgetful and has a lot of domains. When he
was setting up his website he forgot what domain the site had,
but thankfully he had written down the IP address that the
website was on. Now Níels needs to use the IP address to look
up the domain so he can share the site with his friends. To do
this he performs a reverse DNS lookup. But first he needs to
convert his IP address to a PTR record (í. bendilfærslu), but
he needs your help because he’s too busy centering the div on
his website.

## Input
The first line of the input contains a string. This string
will be an IP address of either IPv4 or IPv6 form.

An IPv4 address consists of four parts. Each part is an
integer from and including 0 up to and including 255 These parts are separated by a
single period.

Some examples of valid IPv4 addresses are:

- 10.100.80.13
- 255.255.255.255
- 255.160.134.0

Some examples of invalid IPv4 addresses are:

- 300.1.35.28
- 255.255.255.254.1
- 127,0,0,1

An IPv6 address consists of eight parts. Each part is a four
digit hexadecimal number. These hexadecimal numbers use the
digits from 0 to 9 and the letters from a to f . The eight parts are separated by
single colons. In each part you may omit writing the leading
zeros of the number. If two or more adjacent parts contain the
number 0 they may be
omitted and in their place you write two colons. You are only
allowed to do this in one place in the IP address.

Some examples of valid IPv6 addresses are:

- ffff:dead:1337:beef:4321:f33d:2f92:3419
- 2001:db8:0:0:0:ff00:42:8329
- ::1

Some examples of invalid IPv6 addresses are:

- 0123:4567:89ab:cdef:ghij:klmn:opqr:stuv
- ffff:1234::f6b90::abcd
- 2001:db8:0:0:0:ff00:42:8329:1234

## Output
The output should contain, on a single line, the PTR record
for the IP address.

The PTR record for an IPv4 address is such that the four
parts have been reversed and in-addr.arpa. added to the end.

The PTR record for an IPv6 address is such that the colons
are removed and a single period is placed between each symbol
in the numbers, and that is then reversed. Then .ip6.arpa. is added to the end.

## Scoring
### Sample 1
**Input**
```text
127.0.0.1
```
**Output**
```text
1.0.0.127.in-addr.arpa.
```

### Sample 2
**Input**
```text
2001:db8:0:0:0:ff00:42:8329
```
**Output**
```text
9.2.3.8.2.4.0.0.0.0.f.f.0.0.0.0.0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
```

### Sample 3
**Input**
```text
::1
```
**Output**
```text
1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa.
```
