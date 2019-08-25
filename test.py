#!/usr/bin/python
import seedpart
import random

def do_bip39_test(test, seedlen):
    sobj = seedpart.BIP39xor()
    
    key = ' '.join(sobj._get_random_words(seedlen))
    print('-----------------------------')
    print('Test %s Key' % test)
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
        print('ERROR: split/join failed when shard[2] is unknown')
        return

    sobj2 = seedpart.BIP39xor()
    parts = [None, shard[1], shard[2]]
    sobj2.join(parts)
    print(sobj2)
    if (sobj2.seed != key):
        print('ERROR: split/join failed when shard[0] is unknown')
        return
    
    sobj2 = seedpart.BIP39xor()
    parts = [shard[0], None, shard[2]]
    sobj2.join(parts)
    print(sobj2)
    if (sobj2.seed != key):
        print('ERROR: split/join failed when shard[1] is unknown')
        return

    print('Test %s SUCCESSFUL' % test)

def main():
    random.seed()
    seedlens = [12, 24]
    for i in range(0, 10000):
        seedlen = seedlens[random.randint(0, 1)]
        do_bip39_test(i, seedlen)

main()

