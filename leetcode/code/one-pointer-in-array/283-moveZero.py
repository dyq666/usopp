# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/30 9:28'


class Solution:
    def moveZeroes(self, nums):
        """
        1. 指针内容：值0的位置
        2. 交换条件：当前值不为0时
        """
        try:
            zero_index = nums.index(0)
        except ValueError:
            return
        else:
            for i in range(zero_index + 1, len(nums)):
                if nums[i] != 0:
                    nums[i], nums[zero_index] = nums[zero_index], nums[i]
                    zero_index += 1

    def moveZeroes02(self, nums):
            """
            1. 使用队列记录0的位置
            """
            from collections import deque

            zero_indexes = deque()

            for i, num in enumerate(nums):
                if num == 0:
                    zero_indexes.append(i)
                else:
                    if zero_indexes:
                        zero_index = zero_indexes.popleft()
                        nums[zero_index], nums[i] = num, nums[zero_index]
                        zero_indexes.append(i)
