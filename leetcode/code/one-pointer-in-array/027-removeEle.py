# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/30 9:36'


class Solution:
    def removeElement(self, nums, val):
        """
        1. 283问题变形
        2. 由0变为任意值(val)
        3. 返回的数组中没有val，283中没有这个要求
        """
        try:
            val_index = nums.index(val)
        except ValueError:
            return len(nums)
        else:
            new_len = val_index
            for i in range(val_index+1, len(nums)):
                if nums[i] != val:
                    nums[i], nums[val_index] = nums[val_index], nums[i]
                    val_index += 1
                    new_len += 1
            return new_len
