# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/30 11:45'


class Solution:
    def wordPattern(self, pattern, str):
        """
        1. 保证ab组合的个数，与a的个数，与b的个数都相同
        2. python连等号a == b == c 是 a == b and b == c
        """
        str_list = str.split(' ')
        return len(str_list) == len(pattern) and len(set(zip(str_list, pattern))) == len(set(pattern)) == len(set(str_list))
