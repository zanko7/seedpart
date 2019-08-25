#!/usr/bin/python

import sys
import random
import hashlib

DEFAULT_WORD_FILE        = 'words.txt'
DEFAULT_WORD_FILE_SHA256 = '2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda'
word_list = None

class bip39word:
    '''
    BIP39 word
    Can be initalized with the word string, the word index, or empty.
    '''
    def __init__(self, w = None):
        if type(w) == str:
            self.word = w
            self.num  = self.get_index(w)
            if (self.num == None):
                raise ValueError('BIP39 word "%s" is not valid.' % w)
        elif type(w) == int:
            if ((w > 2047) | (w < 0)):
                raise ValueError('BIP39 word index is %s but must be between 0 and 2047')
            self.word = word_list[w]
            self.num  = w
        else:
            self.word = ''
            self.num  = -1

    def __str__(self):
        return self.word

    def __repr__(self):
        return '<bip39word word:%s num:%s>' % (self.word, self.num)

    def get_index(self, w):
        for i in range(0, len(word_list)):
            if (word_list[i] == w):
                return i
        return None


class bip39shard:
    '''
    BIP39 shard - series of BIP39 words
    Can be initalized with a list of word strings,
    list of word indicies (ints), or empty.
    '''
    def __init__(self, prim_arr=None, length=24):
        if (prim_arr == None):
            '''Initialize empty shard'''
            self.words = [None] * length
        else:
            '''Convert array of int/str to bip39words'''
            self.words = []
            for prim in prim_arr:
                self.words.append(bip39word(prim))

    def __repr__(self):
        return ('<bip38shard length=%s>' % len(self.words))

    def __str__(self):
        return ' '.join(self.get_words())

    def __len__(self):
        return len(self.words)

    def __getitem__(self, idx):
        return self.words[idx]

    def __setitem__(self, idx, val):
        if (type(val) == str):
            self.words[idx] = bip39word(val)
        elif (type(val) == int):
            self.words[idx] = bip39word(val)
        elif type(val) == type(bip39word()):
            self.words[idx] = val

    def reverse(self):
        '''Reverse the list'''
        self.words = self.words[::-1]

    def get_words(self):
        '''Return list of word strings'''
        ret = []
        for i in range(0, len(self.words)):
            if (self.words[i] == None):
                ret.append('')
            else:
                ret.append(self.words[i].word)
        return ret

    def get_indicies(self):
        '''Return list of word indicies (int's)'''
        ret = []
        for i in range(0, len(self.words)):
            if (self.words[i] == None):
                ret.append(-1)
            else:
                ret.append(self.words[i].num)
        return ret


class BIP39xor:
    def __init__(self, word_file = DEFAULT_WORD_FILE):
        global word_list
        word_list = self._load_word_file(word_file)
        if (word_list == None):
            raise Exception('Unable to load word file.')

        self.shard = None
        self.seed  = None

    def __str__(self):
        s = ''

        if (self.shard != None):
            s += '/-------------------------------------------------------------------------------------\\\n'
            s += '|                                seedpart SEED SHARDS                                 |\n'
            s += '|                                                                                     |\n'
            s += '|         SHARD 1           +         SHARD 2             +         SHARD 3           |\n'
            s += '--------------------------- | --------------------------- | ---------------------------\n'
            s += 'Number   Word         Index | Number   Word         Index | Number   Word         Index\n'
            s += '--------------------------- | --------------------------- | ---------------------------\n'
            for i in range(0, len(self.shard[0])):
                s += '{:>6}   {:12} {:>5} | {:>6}   {:12} {:>5} | {:>6}   {:12} {:>5}\n'.format(
                        i+1, self.shard[0].words[i].word, self.shard[0].words[i].num,
                        i+1, self.shard[1].words[i].word, self.shard[1].words[i].num,
                        i+1, self.shard[2].words[i].word, self.shard[2].words[i].num
                    )
            s += '--------------------------- | --------------------------- | ---------------------------\n\n'

        if (self.seed != None):
            s += '/-----------------------------------------------------------\\\n'
            s += '|                       seedpart SEED                       |\n'
            s += '|                                                           |\n'
            s += '-------------------------------------------------------------\n'
            s += 'Number   Word         Index       Number   Word         Index\n'
            s += '---------------------------       ---------------------------\n'
            keys = self.seed.split()
            mid  = int(len(keys)/2)
            for i in range(0, mid):
                a = bip39word(keys[i])
                b = bip39word(keys[i+mid])
                s+= '{:>6}   {:12} {:>5}       {:>6}   {:12} {:>5}\n'.format(
                        i+1,     a.word, a.num,
                        i+mid+1, b.word, b.num
                    )
            s += '---------------------------       ---------------------------\n'

        return s
        

    def _load_word_file(self, word_file):
        '''
        Load the word list from a file.
        If the default word list is used, check sha256.
        '''
        try:
            f = open(word_file, 'r')
            d = f.read()
            
            if (word_file == DEFAULT_WORD_FILE):
                # check sha256 of file
                h = hashlib.new('sha256')
                h.update(str(d).encode('utf-8'))
                if (h.hexdigest() != DEFAULT_WORD_FILE_SHA256):
                    raise Exception('Word file sha256 does not match.')
                    return None

            w = d.splitlines()
            f.close()
            return w
        except:
            raise Exception('Unable to load words file: %s' % word_file)
            return None

    def _get_random_words(self, length):
        '''
        Generate a list of random words of the specified length.
        '''
        ret = []
        random.seed()
        for i in range(0, length):
            ret.append(word_list[random.randint(0, len(word_list)-1)])
        return ret

    def _xor_words(self, shard1, shard2, inverse=0):
        '''
        XOR two bip39shard objects together and return the result.
        If inverse=1, then while doing XORs, one shard increments
        from 0->length while the other shard decrements from length->0.
        '''
        if (len(shard1) != len(shard2)):
            raise Exception('Cannot xor shards of different lengths.')
        
        shard3 = bip39shard(None, len(shard1))
        for i in range(0, len(shard1)):
            if (inverse == 0):
                shard3[i] = bip39word(shard1.words[i].num ^ shard2.words[i].num)
            else:
                shard3[i] = bip39word(shard1.words[i].num ^ shard2.words[len(shard2)-i-1].num)
        return shard3

    def split(self, seed):
        '''
        Split a seed into 3 bip39shard objects.
        The seed should be a single string of words.
        '''
        words         = bip39shard(seed.split())
        entropy       = bip39shard(self._get_random_words(len(words)))
        entropy_xor   = self._xor_words(words, entropy)
        self.shard    = [bip39shard(None, len(words))] * 3
        self.shard[0] = entropy
        self.shard[1] = entropy_xor
        self.shard[2] = self._xor_words(self.shard[0], self.shard[1], 1)
        self.seed     = None

    def join(self, parts):
        '''
        Join 2 of 3 shards together to recover the seed phrase.
        parts can be any combination of:
            bip39shard
            list of ints    (word indicies)
            list of strings (words)
            list of ints mixed with strings
            None            (a missing shard)
        Does not return anything.
        Either print() the bip39xor object or get the .seed string member
        to see the original seed information.
        '''

        # sanity checks
        # - no more than 1 missing
        # - shard lengths must be equal
        missing = -1
        seedlen = -1
        for i in range(0, 3):
            if (parts[i] == None):
                if (missing != -1):
                    raise Exception('Too many missing parts to reconstruct seed.')
                missing = i
            else:
                shardlen = 0
                if type(parts[i]) == str:
                    shardlen = len(parts[i].split())
                elif ((type(parts[i]) == list) | (type(parts[i]) == type(bip39shard()))):
                    shardlen = len(parts[i])
                else:
                    raise Exception('Join parts are of an unknown type.')

                if (seedlen == -1):
                    seedlen = shardlen
                else:
                    if (seedlen != shardlen):
                        raise Exception('Key shards must contain equal number of elements (%s, %s)[index %s].' % (seedlen, len(parts[i]), i))

        if (missing == -1):
            # no parts missing
            return

        # normalize the bip39shard's
        self.shard = [bip39shard(length=seedlen), bip39shard(length=seedlen), bip39shard(length=seedlen)]
        for i in range(0, 3):
            if (parts[i] != None):
                if type(parts[i]) == str:
                    words = parts[i].split()
                    self.shard[i] = bip39shard(words)
                elif type(parts[i]) == list:
                    for x in range(0, len(parts[i])):
                        self.shard[i][x] = parts[i][x]
                elif type(parts[i]) == type(bip39shard()):
                    self.shard[i] = parts[i]

        # reconstruct the missing shard
        if (missing == 0):
            self.shard[missing] = self._xor_words(self.shard[1], self.shard[2], 1)
            self.shard[missing].reverse()
        elif (missing == 1):
            self.shard[missing] = self._xor_words(self.shard[0], self.shard[2])
            self.shard[missing].reverse()
        else:
            self.shard[missing] = self._xor_words(self.shard[0], self.shard[1])

        # reconstruct the seed phrase string
        joinshard = self._xor_words(self.shard[0], self.shard[1])
        self.seed = ''
        for i in range(0, len(joinshard)):
            self.seed += joinshard[i].word
            if (i+1 < len(joinshard)):
                self.seed += ' '

        # drop the shards
        self.shard = None

