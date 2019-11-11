# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/30 11:05'


class Solution:
    def isAnagram(self, s, t):
        from collections import Counter
        return Counter(s) == Counter(t)
