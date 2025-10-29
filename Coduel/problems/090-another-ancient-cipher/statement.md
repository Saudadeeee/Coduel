You have probably heard about the Caesar cipher: It is one
of the most well-known ciphers out there. In an alternative
timeline, the Roman emperor Caesar Augustus builds upon this
cipher to create an encryption even harder to break: The
Augustus cipher.

In the Caesar cipher, you shift each letter by a certain
number of digits forwards or backwards, and start over at the
other side if you roll over. For the English alphabet, the
formulas for encrypting and decrypting the Caesar cipher
are

Where M_ i and C_ i is the ordinal
number of i th letter in
the message and the ciphertext, respectively, and the number n is the integer to
shift by. (The ordinal number of a letter is defined as texttta to 0, textttb to
1, … , textttz to 25 for the Latin
alphabet.)

The Augustus cipher goes above and beyond, and uses a key to encrypt messages. The i th letter of the message is defined
as

If there are more letters in the message than in the key,
the key is repeated. For example, the 4 th 0 -indexed letter of the key key is k ,
the 5 th is e and so on.

Adam has decided to use this cipher for his new social media
platform CyberLounge, and has implemented code to encrypt the
messages with the Augustus cipher. But Adam hasn’t yet found a
way to decrypt the messages! Could you help him with the
decryption algorithm?

## Input
The input consists of two lines. The first line contains the
encrypted string C , and
the second line contains the key K . Both strings contain only
lowercase characters from the Latin alphabet ( a-z ).

## Output
Output the decrypted message.

## Limits
- 0 < |C|, |K| ≤
200

### Sample 1
**Input**
```text
ccvpvygcoyjc
cryptography
```
**Output**
```text
attackatonce
```

### Sample 2
**Input**
```text
tnkkmbwctzhdjesfqugjmgcyzlpxeeyclhg
augustusisthebest
```
**Output**
```text
thequickbrownfoxjumpsoverthelazydog
```

### Sample 3
**Input**
```text
unnmzaxunlzjdzfnnejdx
z
```
**Output**
```text
toolazytomakeagoodkey
```
