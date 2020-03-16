# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/30 12:21'


class Solution:
    def frequencySort(self, s):
        """
        1. 使用most_common来获取频率排序
        """
        from collections import Counter

        return ''.join([k * v for k, v in Counter(s).most_common()])
