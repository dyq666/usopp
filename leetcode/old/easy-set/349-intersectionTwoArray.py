# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/30 9:50'


class Solution:
    def intersection(self, nums1, nums2):
        """
        1. 非常简单的set使用
        """
        nums1_set = set(nums1)
        res = set()

        for num in nums2:
            if num in nums1_set:
                res.add(num)

        return list(res)

    def intersection02(self, nums1, nums2):
        """
        使用python内置的集合操作
        """
        return list(set(nums1) & set(nums2))
