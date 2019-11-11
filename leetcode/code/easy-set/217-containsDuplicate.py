# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/30 18:05'


class Solution:
    def containsDuplicate(self, nums):
        return len(set(nums)) < len(nums)
