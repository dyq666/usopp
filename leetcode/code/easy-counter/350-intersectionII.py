# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/30 10:22'


class Solution:
    def intersect(self, nums1, nums2):
        """
        1. 使用遍历的方式求交集
        """
        from collections import Counter
        nums1_counter = Counter(nums1)
        res = []

        for num in nums2:
            if num in nums1_counter:
                nums1_counter[num] -= 1
                res.append(num)
                if nums1_counter[num] == 0:
                    nums1_counter.pop(num)

        return res

    def intersect02(self, nums1, nums2):
        """
        1. 利用Counter的方法求两个频率dict的交集
        """
        from collections import Counter
        c1, c2 = map(Counter, (nums1, nums2))
        return list((c1 & c2).elements())
