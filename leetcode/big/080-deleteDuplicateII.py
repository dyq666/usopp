# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/30 9:41'


class Solution:
    def removeDuplicates(self, nums):
        """
        1. 指针内容：下一个交换的位置
        2. 交换条件：当前值不等于之前记录的值, 当前值等于记录值但是个数小于2
        """
        cur_val = None
        cur_index = 0
        cur_sum = 0
        new_len = 0

        for num in nums:
            if num != cur_val:
                nums[cur_index] = num
                new_len += 1
                cur_index += 1

                cur_sum = 1
                cur_val = num

            elif cur_sum < 2:
                nums[cur_index] = num
                cur_index += 1
                new_len += 1

                cur_sum += 1

        return new_len
