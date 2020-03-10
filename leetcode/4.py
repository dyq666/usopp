from typing import List

from util import merge_sorted_list


class Solution:
    """核心方法 - 有序数组.

    时间复杂度: O(N)

    先合并两个有序数组, 在找中位数.
    """

    @staticmethod
    def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
        nums = list(merge_sorted_list(nums1, nums2))
        len_ = len(nums)
        if len_ == 0:
            return 0.0
        if len_ & 1 == 1:
            return float(nums[len_ // 2])
        else:
            return (nums[len_ // 2 - 1] + nums[len_ // 2]) / 2


class Solution2:
    """核心方法 - 有序数组.

    直接找中位数.

    TODO 计算本方法的时间复杂度.
    """

    @staticmethod
    def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
        len_ = len(nums1) + len(nums2)
        if len_ == 0:
            return 0.0

        i1, i2 = 0, 0
        pre, cur = 0, 0

        while i1 + i2 != len_ // 2:
            v1 = nums1[i1] if i1 < len(nums1) else float('inf')
            v2 = nums2[i2] if i2 < len(nums2) else float('inf')
            pre = min(v1, v2)
            if v1 < v2:
                i1 += 1
            else:
                i2 += 1

        # 当前索引对应的值, 等于当前两个小索引对应值中的最小值.
        v1 = nums1[i1] if i1 < len(nums1) else float('inf')
        v2 = nums2[i2] if i2 < len(nums2) else float('inf')
        cur = min(v1, v2)
        return float(cur) if len_ & 1 == 1 else (pre + cur) / 2


if __name__ == '__main__':
    fs = [
        Solution.findMedianSortedArrays,
        Solution.findMedianSortedArrays,
    ]

    for f in fs:
        # 数组都为空
        assert f([], []) == 0.0
        assert f([1], []) == 1.0
        # 数组其中之一为空
        assert f([], [1]) == 1.0
        # 数组的所有元素小于或大于另一个数组
        assert f([1, 2], [3, 4]) == 2.5
        assert f([3, 4], [1, 2]) == 2.5
        # 正常情况
        assert f([1, 4], [2, 3]) == 2.5
