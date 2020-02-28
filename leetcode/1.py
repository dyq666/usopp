"""1. Two Sum
Given an array of integers, return indices of the two numbers
such that they add up to a specific target.

You may assume that each input would have exactly one solution,
and you may not use the same element twice.

Example:

> Given nums = [2, 7, 11, 15], target = 9,
>
> Because nums[0] + nums[1] = 2 + 7 = 9,
> return [0, 1].

问题等价于从 Combination(`len(array)`, 2) 的所有组合中找到一组满足条件的组合,
条件为组合内所有元素相加等于 `target`.
"""

from itertools import combinations
from typing import List, Optional


class Solution:

    def twoSum(self, nums: List[int], target: int) -> Optional[List[int]]:
        # 由于 `combinations` 只能返回值, 所以必需反向找索引, 找索引时需注意存在两个值相等
        # 的情况 (因而第二索引必须从第一个索引后面开始找).
        # 此外, 虽然可以自己写两个 for 循环代替 `combinations`, 但第一不能很好的表达
        # 这是一个组合问题, 第二经 LeetCode 测试, `combinations` 的速度比自己写 for 循环
        # 快很多, 因此可以无视 `nums.index` 消耗的时间.
        gen = ([index_one := nums.index(one), nums.index(two, index_one + 1)]
               for one, two in combinations(nums, 2)
               if one + two == target)
        return next(gen, None)
