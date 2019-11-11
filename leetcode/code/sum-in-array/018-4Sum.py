# _*_ coding: utf-8 _*_
__author__ = "dyq666"
__date__ = "2018/5/25 21:03"


class Solution:
    def fourSum(self, nums, target):
        """
        1. O(n^3)
        2. 对于015-3Sum来说外层的循环从一层变为了两层
        3. 每层循环需要干的事情一样
        4. 优化下范围的概念, 比如求四个值, 那么在第一层循环中, 如果数组后面还剩下3个值, 那么应该停止, 后面的每层类推
        """
        nums.sort()
        len_nums = len(nums)
        res = set()

        # 外层由遍历一轮变成遍历两轮
        for i in range(len_nums - 3):

            if i >= 1 and nums[i] == nums[i-1]:
                continue

            for j in range(i+1, len_nums - 2):

                if j >= i + 2 and nums[j] == nums[j-1]:
                    continue

                seen_set = set()

                # 一样的双数的HashSet
                for v_k in nums[j+1:]:
                    search = target - nums[i] - nums[j] - v_k

                    if search in seen_set:
                        res.add((nums[i], nums[j], search, v_k))
                    else:
                        seen_set.add(v_k)

        return list(res)

