

import pickle
import json
from typing import Optional
from avalam import *
from ast import literal_eval as make_tuple


class BoardWithTransposition(Board):
    def flatten(self):
        return [item for sublist in self.m for item in sublist if item != 0]

    def ttentry(self, player: int):
        return "".join(map(str, (player, ) + tuple(self.flatten())))

class TranspositionTable:
    """
    Transposition table from a python dictionary.
    """
    def __init__(self, own_dict=None) -> None:
        self.d = own_dict if own_dict is not None else dict()

    def lookup(self, board: BoardWithTransposition):
        """
        Request the entry in the table, return None if not found.
        """
        return self.d.get(board.ttentry(), None)

    def __call__(self, board: BoardWithTransposition):
        """
        Request the entry in the table, return None if not found.
        """
        return self.d[board.ttentry()]["move"]

    def store(self, **data):
        """
        Store the data in the table.
        """
        entry = data.pop("game").ttentry()
        self.d[entry] = data

    def to_file(self, filename) -> None:
        """
        Save the table to a file. File can be big
        """
        with open(filename, "wb") as f:
            pickle.dump(self.d, f)

    def from_file(self, filename) -> None:
        """
        Load the table from a file.
        """
        with open(filename, "rb") as f:
            self.__dict__.update(pickle.load(f).__dict__)

    def to_json_file(self, filename, use_tuples=False):
        if use_tuples:
            with open(filename, "w") as f:
                k = self.d.keys()
                v = self.d.values()
                k1 = [str(i) for i in k]
                json.dump(dict(zip(*[k1, v])), f, ensure_ascii=False)
        else:
            with open(filename, "w") as f:
                json.dump(self.d, f, ensure_ascii=False)

    def from_json_file(self, filename, use_tuples=False):
        with open(filename, "r") as f:
            data = json.load(f)
            if use_tuples:
                k = data.keys()
                v = data.values()
                k1 = [make_tuple(i) for i in k]
                self.d = dict(zip(*[k1, v]))
            else:
                self.d = data


class HashTranspositionTable:
    """
    Base Class for various types of hashes
    """

    def __init__(self):
        self.modulo = 1024  # default value

    def before(self, key):
        """
        Returns initial value of hash.
        It's also the place where you can initialize some auxiliary variables
        """
        return 0

    def after(self, key, hash):
        """
        Returns final value of hash
        """
        return hash

    def get_hash(self, key, depth=0):
        """
        Recursively computes a hash
        """
        ret_hash = self.before(key)
        if type(key) is int:
            return self.hash_int(key)
        if type(key) is str and len(key) <= 1:
            return self.hash_char(key)
        for v in list(key):
            ret_hash = self.join(ret_hash, self.get_hash(v, depth + 1)) % self.modulo
        if depth == 0:
            ret_hash = self.after(key, ret_hash)
        return ret_hash

    def hash_int(self, number):
        """
        Returns hash for a number
        """
        return number

    def hash_char(self, string):
        """
        Returns hash for an one-letter string
        """
        return ord(string)

    def join(self, one, two):
        """
        Returns combined hash from two hashes
        one - existing (combined) hash so far
        two - hash of new element
        one = join(one, two)
        """
        return (one * two) % self.modulo

class DictTranspositionTable:
    """
    A DictTranspositionTable implements custom dictionary,
    which can be used with transposition tables.
    """

    def __init__(self, num_buckets=1024, own_hash: Optional[HashTranspositionTable]=None):
        """
        Initializes a dictionary with the given number of buckets.
        """
        self.dict = []
        for i in range(num_buckets):
            self.dict.append((None, None))
        self.keys = dict()
        self.hash = hash
        if own_hash is not None:
            own_hash.modulo = len(self.dict)
            self.hash = own_hash.get_hash
        self.num_collisions = 0
        self.num_calls = 0

    def hash_key(self, key):
        """
        Given a key this will create a number and then convert it to
        an index for the dict.
        """
        self.num_calls += 1
        return self.hash(key) % len(self.dict)

    def get_slot(self, key, default=None):
        """
        Returns the index, key, and value of a slot found in the dict.
        Returns -1, key, and default (None if not set) when not found.
        """
        slot = self.hash_key(key)

        if key == self.dict[slot][0]:
            return slot, self.dict[slot][0], self.dict[slot][1]

        return -1, key, default

    def get(self, key, default=None):
        """
        Gets the value for the given key, or the default.
        """
        i, k, v = self.get_slot(key, default=default)
        return v

    def set(self, key, value):
        """
        Sets the key to the value, replacing any existing value.
        """
        slot = self.hash_key(key)

        if self.dict[slot] != (None, None):
            self.num_collisions += 1  # collision occured

        self.dict[slot] = (key, value)

        if self.keys.__contains__(key):
            self.keys[key] = self.keys[key] + 1
        else:
            self.keys[key] = 1

    def delete(self, key):
        """
        Deletes the given key from the dictionary.
        """

        slot = self.hash_key(key)
        self.dict[slot] = (None, None)

        if self.keys.__contains__(key):
            self.keys[key] = self.keys[key] - 1
            if self.keys[key] <= 0:
                del self.keys[key]

    def collisions(self):
        return self.num_collisions

    def __getitem__(self, key):
        return self.get(key)

    def __missing__(self, key):
        return None

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        self.delete(key)

    def __iter__(self):
        return iter(self.keys)

    def __contains__(self, key):
        return self.keys.__contains__(key)

"""
Different types of hashes.
Need to find one that causes the least collisions.
To see the number of collisions, use the DictTranspositionTable.num_collisions
"""

class SimpleHashTranspositionTable(HashTranspositionTable):
    """
    Surprisingly - very effective for strings
    """

    def join(self, one, two):
        return 101 * one + two


class XorHashTranspositionTable(HashTranspositionTable):
    def join(self, one, two):
        return one ^ two


class AddHashTranspositionTable(HashTranspositionTable):
    def join(self, one, two):
        return one + two


class RotateHashTranspositionTable(HashTranspositionTable):
    def join(self, one, two):
        return (one << 4) ^ (one >> 28) ^ two


class BernsteinHashTranspositionTable(HashTranspositionTable):
    def join(self, one, two):
        return 33 * one + two


class ShiftAndAddHashTranspositionTable(HashTranspositionTable):
    def join(self, one, two):
        return one ^ (one << 5) + (one >> 2) + two


class FNVHashTranspositionTable(HashTranspositionTable):
    def before(self, key):
        return 2166136261

    def join(self, one, two):
        return (one * 16777619) ^ two


class OneAtATimeTranspositionTable(HashTranspositionTable):
    def join(self, one, two):
        one += two
        one += one << 10
        return one ^ (one >> 6)

    def after(self, key, hash):
        hash += hash << 3
        hash ^= hash >> 11
        hash += hash << 15
        return hash


class JSWHashTranspositionTable(HashTranspositionTable):
    def before(self, key):
        return 16777551

    def join(self, one, two):
        return (one << 1 | one >> 31) ^ two


class ELFHashTranspositionTable(HashTranspositionTable):
    def before(self, key):
        self.g = 0
        return 0

    def join(self, one, two):
        one = (one << 4) + two
        self.g = one & int("0xF0000000L", 16)

        if self.g != 0:
            one ^= self.g >> 24

        one &= ~self.g
        return (one << 1 | one >> 31) ^ two


class JenkinsHashTranspositionTable(HashTranspositionTable):
    """
    The most advanced hash function on the list.
    Way too many things going on to put something smart in short comment.
    """

    def mix(self, a, b, c):
        """
        Auxiliary function.
        """
        a -= b
        a -= c
        a ^= c >> 13
        b -= c
        b -= a
        b ^= a << 8
        c -= a
        c -= b
        c ^= b >> 13
        a -= b
        a -= c
        a ^= c >> 12
        b -= c
        b -= a
        b ^= a << 16
        c -= a
        c -= b
        c ^= b >> 5
        a -= b
        a -= c
        a ^= c >> 3
        b -= c
        b -= a
        b ^= a << 10
        c -= a
        c -= b
        c ^= b >> 15
        return a, b, c

    def before(self, key):
        self.a = self.b = 0x9E3779B9
        self.c = 0

    def get_hash(self, key, depth=0):
        """
        Overridden.
        Just to create list of single elements to hash
        """
        if depth == 0:
            self.before(key)
        if type(key) is int:
            return [key]
        if type(key) is str and len(key) <= 1:
            return [key]
        tab = []
        for v in list(key):
            tab = tab + self.get_hash(v, depth + 1)
        return self.compute_hash(tab)

    def compute_hash(self, tab):
        """
        Computes real hash
        """
        length = len(tab)
        cur = 0
        while length >= 12:
            self.a += (
                abs(tab[cur + 0])
                + (tab[cur + 1] << 8)
                + (tab[cur + 2] << 16)
                + (tab[cur + 3] << 24)
            )
            self.b += (
                tab[cur + 4]
                + (tab[cur + 5] << 8)
                + (tab[cur + 6] << 16)
                + (tab[cur + 7] << 24)
            )
            self.c += (
                tab[cur + 8]
                + (tab[cur + 9] << 8)
                + (tab[cur + 10] << 16)
                + (tab[cur + 11] << 24)
            )

            self.a, self.b, self.c = self.mix(self.a, self.b, self.c)

            cur += 12
            length -= 12

        self.c += len(tab)

        if length == 11:
            self.c += tab[cur + 10] << 24
        if length == 10:
            self.c += tab[9] << 16
        if length == 9:
            self.c += tab[8] << 8
        if length == 8:
            self.b += tab[7] << 24
        if length == 7:
            self.b += tab[6] << 16
        if length == 6:
            self.b += tab[5] << 8
        if length == 5:
            self.b += tab[4]
        if length == 4:
            self.a += tab[3] << 24
        if length == 3:
            self.a += tab[2] << 16
        if length == 2:
            self.a += tab[1] << 8
        if length == 1:
            self.a += tab[0]

        self.a, self.b, self.c = self.mix(self.a, self.b, self.c)

        return self.c