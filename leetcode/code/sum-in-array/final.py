# _*_ coding: utf-8 _*_
__author__ = "dyq666"
__date__ = "2018/5/25 17:44"


class Solution:

    def __init__(self):
        # 存储最终的结果
        self.res = set()

    def xxSum(self, nums, target):
        """
        1. O(n^(k-1)), k是要加数的个数
        2. 在k为2-5都进行了测试
        3. 只适用于返回所有查找到的的值
        4. 两种方式指针和哈希
        5. 在同等条件下(比如都需要排序数组), 指针方式优于哈希, 因为使用哈希时需要不停的创建一个哈希Set。
        """
        self._start(4, nums, target)

        return list(self.res)

    def _start(self, N_sum, nums, target):
        # 数组排序
        nums.sort()

        # 数组的数量小于加数的个数, 加数的个数小于2, 目标值比数组中最小的N倍还小, 目标值比数组中最大的N倍还大。这四种都是无效的
        if len(nums) < N_sum or N_sum < 2 or target < nums[0] * N_sum or target > nums[-1] * N_sum:
            return

        # 4个数的合就需要外层两层循环(类推5需要3层..), 还需要初始化一个同样大小的存储每层循环中索引
        self._for_nested(N_sum - 2, nums, 0, target, [None] * (N_sum - 2))

    def _for_nested(self, N, nums, start, target, saved_items):

        # 如果循环次数为0, 则使用指针或者哈希查找target
        if N == 0:
            # 获取所有前面循环的索引对应的值
            # all_value = [nums[i] for i in reversed(all_index)]
            target = target - sum(saved_items)

            # 两种查找target的方式
            self._find_sum_by_pointer(nums, start, target, list(reversed(saved_items)))
            # self._find_sum_by_hash(nums, start, target, list(reversed(saved_items)))

        else:

            for i in range(start, len(nums) - (N + 1)):
                # 从第二个开始, 如果值与前一个值相同则continue, 因为相同的值往下面进行循环是无意义的
                if i >= start + 1 and nums[i] == nums[i - 1]:
                    continue

                # 在对应的位置存储当前循环对应的索引
                saved_items[N - 1] = nums[i]

                self._for_nested(N - 1, nums, i + 1, target, saved_items)

    def _find_sum_by_hash(self, nums, left_start, target, saved_items):
        """
        1. 使用hash的方法
        2. 根据要查找的值, 将所有可能的组合存到self.res
        3. 参数说明 nums-原始数组的一部, 起始点, 查找的目标, 要存储的值
        """
        seen_set = set()

        for num in nums[left_start:]:
            # 如果找到目标就存储到结果集合(res)，没找到就将值加入已经遍历过的集合(seen_set)
            search = target - num
            if search in seen_set:
                self.res.add((*saved_items, search, num))
            else:
                seen_set.add(num)

    def _find_sum_by_pointer(self, nums, left_start, target, saved_items):
        """
        1. 使用双指针来寻找值
        2. 根据要查找的值, 将所有可能的组合存到self.res
        3. 参数说明 nums-原始的数组, 起始点, 查找的目标, 要存储的值
        """
        left, right = left_start, len(nums) - 1

        while left < right:
            two_sum = nums[left] + nums[right]

            if two_sum < target:
                left += 1
            elif two_sum > target:
                right -= 1
            else:  # 找到了
                self.res.add((*saved_items, nums[left], nums[right]))

                # 两端都移动, 如果移动后值未改变则继续移动
                left += 1
                right -= 1

                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1

