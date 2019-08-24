#!/usr/bin/python

import sys
import hashlib

DEFAULT_WORD_FILE        = 'words.txt'
DEFAULT_WORD_FILE_SHA256 = '2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda'
word_list = None

class bip39word:
    def __init__(self, w = None):
        if type(w) == str:
            self.word = w
            self.num  = self.get_index(w)
        elif type(w) == int:
            self.word = word_list[w]
            self.num  = w
        else:
            self.word = ''
            self.num  = -1

    def get_index(self, w):
        for i in range(0, len(word_list)):
            if (word_list[i] == w):
                return i
        return None

    def __str__(self):
        return self.word

    def __repr__(self):
        return '<bip39word word:%s num:%s>' % (self.word, self.num)

class BIP39xor:
    def __init__(self, word_file = DEFAULT_WORD_FILE):
        global word_list
        word_list = self._load_word_file(word_file)
        if (word_list == None):
            raise Exception('Unable to load word file.')

        self.part = None
        self.seed = None

    def __str__(self):
        s = ''

        if (self.part != None):
            s += '/-------------------------------------------------------------------------------------\\\n'
            s += '|                                 seedpart SEED PARTS                                 |\n'
            s += '|                                                                                     |\n'
            s += '|           KEY 1           +           KEY 2             +           KEY 3           |\n'
            s += '--------------------------- | --------------------------- | ---------------------------\n'
            s += 'Number   Word         Index | Number   Word         Index | Number   Word         Index\n'
            s += '--------------------------- | --------------------------- | ---------------------------\n'
            for i in range(0, len(self.part[0])):
                s += '{:>6}   {:12} {:>5} | {:>6}   {:12} {:>5} | {:>6}   {:12} {:>5}\n'.format(
                        i+1, self.part[0][i].word, self.part[0][i].num,
                        i+1, self.part[1][i].word, self.part[1][i].num,
                        i+1, self.part[2][i].word, self.part[2][i].num
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
        

    '''
    Load the word list from a file.
    If the default word list is used, check sha256.
    '''
    def _load_word_file(self, word_file):
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


    def split(self, seed):
        self.seed = seed
        self.part = [[], [], []]
        words     = seed.split()
        middle    = int(len(words)/2)

        for w in words[0:middle]:
            self.part[0].append(bip39word(w))
        for w in words[middle:]:
            self.part[1].append(bip39word(w))
        
        if (len(self.part[0]) != len(self.part[1])):
            raise Exception('Seed word length not even.')

        for i in range(0, len(self.part[0])):
            self.part[2].append(bip39word(self.part[0][i].num ^ self.part[1][i].num))

    def join(self, parts):
        self.part = [[], [], []]
        missing = -1
        for i in range(0, 3):
            if (parts[i] == None):
                if (missing != -1):
                    raise Exception('Too many missing parts to reconstruct seed.')
                missing = i
            else:
                if type(parts[i]) == str:
                    words = parts[i].split()
                    for w in words:
                        self.part[i].append(bip39word(w))
                elif type(parts[i]) == list:
                    for obj in parts[i]:
                        if type(obj) == str:
                            self.part[i].append(bip39word(obj))
                        elif type(obj) == type(bip39word()):
                            self.part[i].append(obj)
                else:
                    raise Exception('Join parts are of unknown type.')

        if (missing == -1):
            # no parts missing
            return

        self.part[missing] = []
        a = b = 0
        if (missing == 0):   a = 1; b = 2
        elif (missing == 1): a = 0; b = 2
        elif (missing == 2): a = 0; b = 1

        for i in range(0, len(self.part[a])):
            self.part[missing].append(bip39word(self.part[a][i].num ^ self.part[b][i].num))

        self.seed = ''
        for p in range(0, 2):
            for i in range(0, len(self.part[p])):
                self.seed += self.part[p][i].word + ' '

        return



