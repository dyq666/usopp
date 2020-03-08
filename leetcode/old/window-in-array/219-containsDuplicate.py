# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/30 17:56'


class Solution:
    def containsNearbyDuplicate(self, nums, k):
        """
        1. 滑动条件：窗口是否满足元素个数 - 1 < k ， 满足右边界动，否则左边界动，右边界动时需要判断将要吃进来的值是否在窗口中
        """

        left, right = 0, -1

        window_set = set()

        while left < len(nums):

            if right - left < k and right + 1 < len(nums):
                if nums[right + 1] in window_set:
                    return True
                window_set.add(nums[right + 1])
                right += 1

            else:
                window_set.remove(nums[left])
                left += 1

        return False
