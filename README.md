# seedpart

Michael Laforest `<mjlaforest` *at* `gmail` *dot* `com>`


# Support

Donation Method | Address | QR Code
--- | --- | ---
Bitcoin Cash (BCH) | 1HSycjR3LAZxuLG34aEBbQdUSayPkh8XsH | ![1HSycjR3LAZxuLG34aEBbQdUSayPkh8XsH](https://raw.github.com/MJL85/natlas/master/docs/donate/BCH.png "Bitcoin Cash (BCH)")
Bitcoin (BTC) | 1HY3jPYVfE6YZbuYTYfMpazvSKRXjZDMbS  | ![1HY3jPYVfE6YZbuYTYfMpazvSKRXjZDMbS](https://raw.github.com/MJL85/natlas/master/docs/donate/BTC.png "Bitcoin (BTC)")

# About

Some people may want to store their BIP39 keys in a secured physical location.  There are several options available, with some of the most popular being:

1. Store the full 24 word private seed on Cryptosteel or a similar product. This means the bearer has **100%** of the seed phrase and access to the coins.  
  
1. Split the 24 words up into three sets of 8 words, A, B, and C. You could then put A+B on one Cryptosteel, B+C on another, and A+C on a third.  Two of three sets are required to recover the original seed.  The bearer of any of these has **66%** of the seed phrase.  
  
1. Split the key into two parts, A and B.  Create a new set of 12 words, C, where `C = A xor B`. Two of three sets are required to recover the original seed.  The bearer of any of these has **50%** of the seed phrase.

1. Shamir secret sharing or a similar algortihm could be used to protect the key in a significantly stronger manner.  However, these methods may be too difficult for non-technical family member or next of kin to recover in an emergency without the creators assistance.
  
*seedpart* implements the XOR process from option #3.

# Example Usage

## Splitting a Seed Phrase
```python
>>> import seedpart
>>> key = 'thank equip quality viable merit garden phone jeans mansion pilot grant toddler crisp velvet ability aim dutch camp actor coconut negative thought color involve'
>>> sp = seedpart.BIP39xor()
>>> sp.split(key)
>>> print(sp)
```
```
/-------------------------------------------------------------------------------------\
|                                 seedpart SEED PARTS                                 |
|                                                                                     |
|           KEY 1           +           KEY 2             +           KEY 3           |
--------------------------- | --------------------------- | ---------------------------
Number   Word         Index | Number   Word         Index | Number   Word         Index
--------------------------- | --------------------------- | ---------------------------
     1   thank         1790 |      1   crisp         1790 |      1   unaware       1790
     2   equip          609 |      2   velvet         609 |      2   sail           609
     3   quality       1401 |      3   ability       1401 |      3   pyramid       1401
     4   viable        1946 |      4   aim           1946 |      4   voyage        1946
     5   merit         1116 |      5   dutch         1116 |      5   soup          1116
     6   garden         765 |      6   camp           765 |      6   legal          765
     7   phone         1308 |      7   actor         1308 |      7   patrol        1308
     8   jeans          957 |      8   coconut        957 |      8   forget         957
     9   mansion       1082 |      9   negative      1082 |      9   believe       1082
    10   pilot         1319 |     10   thought       1319 |     10   dune          1319
    11   grant          813 |     11   color          813 |     11   elite          813
    12   toddler       1819 |     12   involve       1819 |     12   next          1819
--------------------------- | --------------------------- | ---------------------------

/-----------------------------------------------------------\
|                       seedpart SEED                       |
|                                                           |
-------------------------------------------------------------
Number   Word         Index       Number   Word         Index
---------------------------       ---------------------------
     1   thank         1790           13   crisp          413
     2   equip          609           14   velvet        1936
     3   quality       1401           15   ability          1
     4   viable        1946           16   aim             42
     5   merit         1116           17   dutch          547
     6   garden         765           18   camp           262
     7   phone         1308           19   actor           21
     8   jeans          957           20   coconut        359
     9   mansion       1082           21   negative      1183
    10   pilot         1319           22   thought       1799
    11   grant          813           23   color          365
    12   toddler       1819           24   involve        945
---------------------------       ---------------------------
```
# Reconstructing the Seed from Two Parts
```python
>>> import seedpart
>>> sp2 = seedpart.BIP39xor()
>>> parts = [ 'thank equip quality viable merit garden phone jeans mansion pilot grant toddler', None, 'unaware sail pyramid voyage soup legal patrol forget believe dune elite next' ]
>>> sp.join(parts)
>>> print(sp)
```
```
/-------------------------------------------------------------------------------------\
|                                 seedpart SEED PARTS                                 |
|                                                                                     |
|           KEY 1           +           KEY 2             +           KEY 3           |
--------------------------- | --------------------------- | ---------------------------
Number   Word         Index | Number   Word         Index | Number   Word         Index
--------------------------- | --------------------------- | ---------------------------
     1   thank         1790 |      1   crisp         1790 |      1   unaware       1790
     2   equip          609 |      2   velvet         609 |      2   sail           609
     3   quality       1401 |      3   ability       1401 |      3   pyramid       1401
     4   viable        1946 |      4   aim           1946 |      4   voyage        1946
     5   merit         1116 |      5   dutch         1116 |      5   soup          1116
     6   garden         765 |      6   camp           765 |      6   legal          765
     7   phone         1308 |      7   actor         1308 |      7   patrol        1308
     8   jeans          957 |      8   coconut        957 |      8   forget         957
     9   mansion       1082 |      9   negative      1082 |      9   believe       1082
    10   pilot         1319 |     10   thought       1319 |     10   dune          1319
    11   grant          813 |     11   color          813 |     11   elite          813
    12   toddler       1819 |     12   involve       1819 |     12   next          1819
--------------------------- | --------------------------- | ---------------------------

/-----------------------------------------------------------\
|                       seedpart SEED                       |
|                                                           |
-------------------------------------------------------------
Number   Word         Index       Number   Word         Index
---------------------------       ---------------------------
     1   thank         1790           13   crisp          413
     2   equip          609           14   velvet        1936
     3   quality       1401           15   ability          1
     4   viable        1946           16   aim             42
     5   merit         1116           17   dutch          547
     6   garden         765           18   camp           262
     7   phone         1308           19   actor           21
     8   jeans          957           20   coconut        359
     9   mansion       1082           21   negative      1183
    10   pilot         1319           22   thought       1799
    11   grant          813           23   color          365
    12   toddler       1819           24   involve        945
---------------------------       ---------------------------
```

# By Hand

You could do this process by hand with the following procedure:  
1. Convert each of the seed words to the line number they appear in the word list.
1. Split the list of numbers into two equal lists, A and B.
1. For each word in the two lists, calculate `A xor B` to produce the third list, C.
1. To reconstruct given lists A&C or B&C, repeat step 3. (eg, if `A xor B = C` then `A xor C = B` and `B xor C = A`)

