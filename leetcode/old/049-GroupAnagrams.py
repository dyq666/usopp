# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/30 12:51'


class Solution:
    def groupAnagrams(self, strs):
        """
        1. fronzendict = fronzenset((k, v) for k, v in dict.items())
        """
        from collections import Counter

        hash_map = {}

        for s in strs:
            hash_map.setdefault(frozenset(((k, v) for k, v in Counter(s).items())), []).append(s)

        return list(hash_map.values())

    def groupAnagrams(self, strs):
        """
        1. 主要问题是解决如何选择map的key
        """
        hash_map = {}

        for s in strs:
            hash_map.setdefault(tuple(sorted(s)), []).append(s)

        return list(hash_map.values())
