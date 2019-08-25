# seedpart

Michael Laforest `<mjlaforest` *at* `gmail` *dot* `com>`

# About

seedpart will take a 12 or 24 word seed and generate three different seeds of the same length.  
Two of the three generated seeds can be used to recover the original seed phrase.  
  
The process uses a series of XOR operations along with some entropy data to generate shards which do not expose any part of the original seed phrase.

# Example Usage

## Splitting a Seed Phrase
```python
# python
>>> import seedpart
>>> key = 'thank equip quality viable merit garden phone jeans mansion pilot grant toddler crisp velvet ability aim dutch camp actor coconut negative thought color involve'
>>> sp = seedpart.BIP39xor()
>>> sp.split(key)
>>> print(sp)
```
```
/-------------------------------------------------------------------------------------\
|                                seedpart SEED SHARDS                                 |
|                                                                                     |
|         SHARD 1           +         SHARD 2             +         SHARD 3           |
--------------------------- | --------------------------- | ---------------------------
Number   Word         Index | Number   Word         Index | Number   Word         Index
--------------------------- | --------------------------- | ---------------------------
     1   noble         1197 |      1   engine         595 |      1   ensure         602
     2   outer         1258 |      2   sphere        1675 |      2   require       1464
     3   repair        1460 |      3   boost          205 |      3   lazy          1011
     4   slow          1633 |      4   disorder       507 |      4   apart           82
     5   health         849 |      5   ticket        1805 |      5   beef           160
     6   guard          826 |      6   decline        455 |      6   elite          576
     7   tag           1769 |      7   leaf          1013 |      7   swear         1756
     8   witness       2021 |      8   mention       1112 |      8   knock          990
     9   gas            768 |      9   trap          1850 |      9   retire        1471
    10   awful          133 |     10   reform        1442 |     10   pill          1318
    11   chapter        307 |     11   duck           542 |     11   road          1495
    12   glory          796 |     12   liberty       1031 |     12   tenant        1784
    13   monkey        1145 |     13   route         1508 |     13   average        126
    14   hub            884 |     14   orient        1252 |     14   coil           362
    15   reform        1442 |     15   refuse        1443 |     15   abandon          0
    16   sport         1685 |     16   subject       1727 |     16   curious        431
    17   seek          1560 |     17   manual        1083 |     17   elite          576
    18   chapter        307 |     18   allow           53 |     18   flee           710
    19   combine        367 |     19   consider       378 |     19   bench          168
    20   fan            662 |     20   lawsuit       1009 |     20   recall        1435
    21   few            684 |     21   shoe          1587 |     21   helmet         855
    22   chimney        320 |     22   similar       1607 |     22   coyote         397
    23   among           63 |     23   clean          338 |     23   story         1716
    24   potato        1350 |     24   ten           1783 |     24   tired         1813
--------------------------- | --------------------------- | ---------------------------
```
# Reconstructing the Seed from Two Parts
```python
# python
>>> import seedpart
>>> sp = seedpart.BIP39xor()
>>> shard1 = 'noble outer repair slow health guard tag witness gas awful chapter glory monkey hub reform sport seek chapter combine fan few chimney among potato'
>>> shard2 = 'engine sphere boost disorder ticket decline leaf mention trap reform duck liberty route orient refuse subject manual allow consider lawsuit shoe similar clean ten'
>>> sp.join([shard1, shard2, None])
>>> print(sp)
```
```
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

# Reconstructing By Hand

You can reconstruct the seed by hand with the following procedure:  
1. Convert each shard into a list of numbers, where each number is the line the word appears in the BIP39 list minus 1 (e.g. "abondon" = 0, "monkey" = 1145).
1. If you are missing shard 0:
    1. XOR each number from both shards to generate a third shard. For shard 1, start with the first word and work down. For shard 2, start with the last shard and work backwards.
	1. Reverse the list generated from the previous step.
1. If you are missing shard 1:
    1. XOR each number from both shards to generate a third shard. For both shards start with the first word.
	1. Reverse the list generated from the previous step.
1. If you are missing shard 2:
    1. XOR each number from both shards to generate a third shard. For both shards start with the first word.
1. XOR shard 0 and shard 1 to recover the original seed phrase.

# Support

Donation Method | Address | QR Code
--- | --- | ---
Bitcoin Cash (BCH) | 1HSycjR3LAZxuLG34aEBbQdUSayPkh8XsH | ![1HSycjR3LAZxuLG34aEBbQdUSayPkh8XsH](https://raw.github.com/MJL85/natlas/master/docs/donate/BCH.png "Bitcoin Cash (BCH)")
Bitcoin (BTC) | 1HY3jPYVfE6YZbuYTYfMpazvSKRXjZDMbS  | ![1HY3jPYVfE6YZbuYTYfMpazvSKRXjZDMbS](https://raw.github.com/MJL85/natlas/master/docs/donate/BTC.png "Bitcoin (BTC)")
