# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/30 11:49'


class Solution:
    def isIsomorphic(self, s, t):
        """
        1. 和290一样
        """
        return len(s) == len(t) and len(set(zip(s, t))) == len(set(s)) == len(set(t))
