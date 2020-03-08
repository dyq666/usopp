# _*_ coding: utf-8 _*_
__author__ = "dyq666"
__date__ = "2018/5/25 21:12"


class Solution:
    def threeSumClosest(self, nums, target):
        """
        1. O(n^2)
        2. 不能使用hash, 因为不是准确的查询
        3. 思路基本与015中相同
        """
        nums.sort()
        res = sum(nums[:3])

        for i, v_i in enumerate(nums):
            if i >= 1 and v_i == nums[i - 1]:
                continue

            left, right = i + 1, len(nums) - 1

            while left < right:

                three_sum = nums[left] + nums[right] + v_i
                if abs(target - three_sum) < abs(target - res):
                    res = three_sum

                if three_sum == target:
                    return three_sum

                if three_sum < target:
                    left += 1
                else:
                    right -= 1

        return res
