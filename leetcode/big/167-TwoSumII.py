# _*_ coding: utf-8 _*_
__author__ = "dyq666"
__date__ = "2018/5/26 7:49"


class Solution:
    def twoSum(self, numbers, target):
        """
        1. O(n)
        2. 双指针
        """
        left, right = 0, len(numbers) - 1

        while left < right:

            two_sum = numbers[left] + numbers[right]

            if target > two_sum:
                left += 1
            elif target < two_sum:
                right -= 1
            else:
                return [left + 1, right + 1]

    def twoSum02(self, numbers, target):
        """
        1. O(n)
        2. 哈希
        """

        seen_dict = {}

        for i, v_i in enumerate(numbers):

            search = target - v_i
            if search in seen_dict:
                return [seen_dict[search] + 1, i + 1]
            else:
                seen_dict[v_i] = i
