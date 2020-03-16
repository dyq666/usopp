# _*_ coding: utf-8 _*_
__author__ = "dyq666"
__date__ = "2018/5/25 20:39"


class Solution:
    def threeSum(self, nums):
        """
        1. O(n^2)
        2. 基础001中的双指针思想, 相当于执行n次001中的双指针的遍历, 每次的target不同而已.
        3. 这里需要找多个值, 所以在找到值后需要将两个指针都向里面移动, 移动到值不同的地方.
           举个例子: 1 + 2 + 3 = 0, 在1不变的情况下, 2和3都必须改变才能保证得到一组不同的值并且还满足这个等式
        4. (优化)在每次执行遍历前, 必须判断当前值是否与上一个值相同, 如果相同就不执行后面的内容.
           举个例子: [1, 1, 2, 3, 4], 当第一个1被遍历完了之后, 到第二个1继续遍历, target是不变的, 而相同的target下后面每个组合都被寻找过了.
        """
        # 排序
        nums.sort()

        res = set()

        for i, v_i in enumerate(nums):
            # 优化部分
            if i >= 1 and v_i == nums[i - 1]:
                continue

            left, right = i + 1, len(nums) - 1

            while left < right:
                two_sum = nums[left] + nums[right]
                target = -v_i

                if two_sum > target:
                    right -= 1
                elif two_sum < target:
                    left += 1
                else:
                    res.add((v_i, nums[left], nums[right]))

                    left += 1
                    right -= 1

                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1

        return list(res)

    def threeSum02(self, nums):
        """
        1. O(n^2)
        2. 与1基本类似, 除了将双指针变成001中的hash
        """
        nums.sort()
        res = set()

        for i, v_i in enumerate(nums[:-2]):

            if i >= 1 and v_i == nums[i - 1]:
                continue

            seen_set = set()
            for num in nums[i + 1:]:

                search = 0 - (v_i + num)
                if search in seen_set:
                    res.add((v_i, search, num))
                else:
                    seen_set.add(num)

        return list(res)
