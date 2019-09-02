#!/usr/bin/python
import seedpart
import random

def do_bip39_test(test, seedlen, key = None):
    sobj = seedpart.BIP39xor()
    
    if (key == None):
        key = ' '.join(sobj._get_random_words(seedlen))
    print('-----------------------------')
    print('BIP39xor Test %s Key' % test)
    print(key)
    print('-----------------------------')

    sobj.split(key)
    print(sobj)

    shard = [
                sobj.shard[0].get_indicies(),           # list of indicies
                sobj.shard[1],                          # bip39shard object
                ' '.join(sobj.shard[2].get_words())     # single string of words
            ]

    sobj2 = seedpart.BIP39xor()
    parts = [shard[0], shard[1], None]
    sobj2.join(parts)
    print(sobj2)
    if (sobj2.seed != key):
        print('ERROR: BIP39xor split/join failed when shard[2] is unknown')
        return

    sobj2 = seedpart.BIP39xor()
    parts = [None, shard[1], shard[2]]
    sobj2.join(parts)
    print(sobj2)
    if (sobj2.seed != key):
        print('ERROR: BIP39xor split/join failed when shard[0] is unknown')
        return
    
    sobj2 = seedpart.BIP39xor()
    parts = [shard[0], None, shard[2]]
    sobj2.join(parts)
    print(sobj2)
    if (sobj2.seed != key):
        print('ERROR: BIP39xor split/join failed when shard[1] is unknown')
        return

    print('BIP39xor Test %s SUCCESSFUL' % test)

def do_plaintext_test(test, key = None):
    sobj   = seedpart.plaintextxor()

    if (key == None):
        keylen = random.randrange(20, 100)
        key    = sobj._intarr_to_str(sobj._get_random_data(keylen))

    print('-----------------------------')
    print('PlainTextXOR Test %s Key' % test)
    print(key)
    print('-----------------------------')
    sobj.split(key)
    print(sobj)

    sobj2 = seedpart.plaintextxor()
    sobj2.join([sobj.shard[0], sobj.shard[1], None])
    print(sobj2)
    if (sobj2.key != key):
        print('ERROR: PlainTextXOR split/join failed when shard[0] is unknown')

    sobj2.join([sobj.shard[0], None,          sobj.shard[2]])
    print(sobj2)
    if (sobj2.key != key):
        print('ERROR: PlainTextXOR split/join failed when shard[0] is unknown')

    sobj2.join([None,          sobj.shard[1], sobj.shard[2]])
    print(sobj2)
    if (sobj2.key != key):
        print('ERROR: PlainTextXOR split/join failed when shard[0] is unknown')
    
    print('PlainTextXOR Test %s SUCCESSFUL' % test)

def main():
    random.seed()
    seedlens = [12, 24]
    for i in range(0, 1000):
        seedlen = seedlens[random.randint(0, 1)]
        do_bip39_test(i, seedlen)

    for i in range(0, 1000):
        do_plaintext_test(i)

main()

