#!/usr/bin/python
import sys
import string
import random

PLAINTEXTXOR_VER = 'seedpart(plaintextxor) v0.1'

class plaintextxor:

    def __init__(self):
        self.shard = None
        self.key   = None
        return

    def __str__(self):
        if (self.key != None):
            return 'Plaintext key: %s' % self.key
        elif (self.shard != None):
            s  = 'Shard 1: %s\n' % self._intarr_to_hexstr(self.shard[0])
            s += 'Shard 2: %s\n' % self._intarr_to_hexstr(self.shard[1])
            s += 'Shard 3: %s'   % self._intarr_to_hexstr(self.shard[2])
            return s

    def _xor_keys(self, shard1, shard2):
        if (len(shard1) != len(shard2)):
            raise Exception('Cannot xor shards of different lengths.')
        
        shard3 = []
        for i in range(0, len(shard1)):
            shard3.append(shard1[i] ^ shard2[i])
        return shard3

    def _str_to_intarr(self, s):
        h = []
        for i in range (0, len(s)):
            h.append(ord(s[i]))
        return h

    def _hexstr_to_intarr(self, s):
        h = []
        for i in range(0, len(s), 2):
            h.append(int(s[i:i+2], 16))
        return h

    def _intarr_to_hexstr(self, arr):
        ret = ''
        for i in arr:
            ret += format(i, '02x')
        return ret
    
    def _intarr_to_str(self, arr):
        ret = ''
        for i in arr:
            ret += chr(i)
        return ret

    def _get_random_data(self, slen):
        chars = string.ascii_letters + string.digits + string.punctuation
        random.seed()
        ret = []
        for i in range(0, slen):
            ret.append(ord(random.choice(chars)))
        return ret

    def split(self, key):
        entropy = self._get_random_data(len(key))
        ikey    = self._str_to_intarr(key)

        self.shard    = [[], [], []]
        self.shard[0] = entropy
        self.shard[1] = self._xor_keys(ikey, entropy)
        self.shard[2] = self._xor_keys(self.shard[0], self.shard[1][::-1])
        self.key      = None

    def join(self, parts):
        # sanity checks
        # - no more than 1 missing
        # - shard lengths must be equal
        missing = -1
        keylen  = -1
        for i in range(0, 3):
            if (parts[i] == None):
                if (missing != -1):
                    raise Exception('Too many missing parts to reconstruct seed.')
                missing = i
            else:
                shardlen = len(parts[i]) / 2
                if (keylen == -1):
                    keylen = shardlen
                else:
                    if (keylen != shardlen):
                        raise Exception('Key shards must contain equal number of elements (%s, %s)[index %s].' % (keylen, len(parts[i]), i))

        if (missing == -1):
            # no parts missing
            return

        # normalize the shards
        self.shard = [None, None, None]
        for i in range(0, 3):
            if (parts[i] != None):
                if (type(parts[i]) == str):
                    self.shard[i] = self._hexstr_to_intarr(parts[i])
                elif (type(parts[i]) == list):
                    self.shard[i] = parts[i]
                else:
                    raise TypeError('Key shard %i is of unknown type (%s).' % (i, type(parts[i])))

        # reconstruct the missing shard
        if (missing == 0):
            self.shard[missing] = self._xor_keys(self.shard[1][::-1], self.shard[2])
        elif (missing == 1):
            self.shard[missing] = self._xor_keys(self.shard[0][::-1], self.shard[2][::-1])
        else:
            self.shard[missing] = self._xor_keys(self.shard[0], self.shard[1])

        # reconstruct the seed phrase string
        joinshard = self._xor_keys(self.shard[0], self.shard[1])
        self.key = ''
        for i in range(0, len(joinshard)):
            self.key += chr(joinshard[i])

        # drop the shards
        self.shard = None

