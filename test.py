#!/usr/bin/python
import seedpart

def main():
    sobj = seedpart.BIP39xor()
    
    key = 'repeat country fall fortune garlic opera whale frost talk blush balance kick harvest large wonder potato stairs shaft focus client food round inject off'
    sobj.split(key)
    print(sobj)

    print('\n\n\n')

    sobj2 = seedpart.BIP39xor()
    parts = [
                'repeat country fall fortune garlic opera whale frost talk blush balance kick',
                'harvest large wonder potato stairs shaft focus client food round inject off',
                None
            ]
    sobj2.join(parts)
    print(sobj2)
    parts = [
                'repeat country fall fortune garlic opera whale frost talk blush balance kick',
                None,
                'thank equip quality viable merit garden phone jeans mansion pilot grant toddler'
            ]
    sobj2.join(parts)
    print(sobj2)
    parts = [
                None,
                'harvest large wonder potato stairs shaft focus client food round inject off',
                'thank equip quality viable merit garden phone jeans mansion pilot grant toddler'
            ]
    sobj2.join(parts)
    print(sobj2)

    parts = [
                sobj.part[0],
                'harvest large wonder potato stairs shaft focus client food round inject off',
                None
            ]
    sobj2.join(parts)
    print(sobj2)
    
    parts = [
                sobj.part[0],
                [ 'harvest', 'large', 'wonder', 'potato', 'stairs', 'shaft', 'focus', 'client', 'food', 'round', 'inject', 'off' ],
                None
            ]
    sobj2.join(parts)
    print(sobj2)

main()

