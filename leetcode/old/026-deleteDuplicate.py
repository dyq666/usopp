# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/30 9:39'


class Solution:
    def removeDuplicates(self, nums):
        """
        1. 指针内容：下一个交换的位置
        2. 交换条件：当前值不等于之前记录的值
        """
        cur_val = None
        cur_index = 0
        new_len = 0

        for num in nums:
            if num != cur_val:
                nums[cur_index] = num
                cur_index += 1
                cur_val = num
                new_len += 1

        return new_len
