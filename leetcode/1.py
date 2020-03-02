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
"""

from itertools import combinations
from operator import itemgetter
from typing import List, Optional, Tuple


class Solution:
    """核心方法 - Combination.

    问题等价于从 Combination(`len(array)`, 2) 的所有组合中找到一组满足条件的组合,
    条件为组合内所有元素相加等于 `target`.
    """

    @staticmethod
    def twoSum(nums: List[int], target: int) -> Optional[List[int]]:
        # 由于 `combinations` 只能返回值, 所以必需反向找索引, 找索引时需注意存在两个值相等
        # 的情况 (因而第二索引必须从第一个索引后面开始找).
        # 此外, 虽然可以自己写两个 for 循环代替 `combinations`, 但第一不能很好的表达
        # 这是一个组合问题, 第二经 LeetCode 测试, `combinations` 的速度比自己写 for 循环
        # 快很多, 因此可以无视 `nums.index` 消耗的时间.
        gen = ([index1 := nums.index(one), nums.index(two, index1 + 1)]
               for one, two in combinations(nums, 2)
               if one + two == target)
        return next(gen, None)


class Solution2:
    """核心方法 - Hash.

    这是本题最巧妙的解法, 完美的利用了 hash O(1) 的时间复杂度. 但是很难想到这种解法,
    在此想办法我将这个解法变得更通用化. 如果想利用一次循环找到两个符合规则的值, 那么前
    面遇到的元素, 必定有某种属性可以被后面的元素所使用.

    在本例中, 每个元素都会告诉后面元素它需要某个值和它配对, 实际上还可以在 `needs` 中
    存储元素本身的值, 这时相当于询问后面的元素能否合我配对.

    另外这个解法比较容易想到的中间版本 `twoSum02`. 此解法中, 第一次遍历记录了所有元
    素的需求, 第二次遍历在查找是否满足了元素的需求. 两种解法都是 O(n) 的, 不会有很大
    差距. 另外这个解法中需要小心第二次遍历中元素本身是不能满足自己的需求.
    """

    @staticmethod
    def twoSum(nums: List[int], target: int) -> Optional[List[int]]:
        # 取名 `needs` 的原因: 它存储的是已经遍历过的元素的需求 (元素想要一个什么值).
        needs = {}
        for i, num in enumerate(nums):
            if num in needs:
                return [needs[num], i]
            needs[target - num] = i

    @staticmethod
    def twoSum02(nums: List[int], target: int) -> Optional[List[int]]:
        # `twoSum` 的一个中间版本. 具体用途看类的 `doc`.
        needs = {(target - num): i for i, num in enumerate(nums)}
        gen = ([needs[num], i]
               for i, num in enumerate(nums)
               if num in needs and i != needs[num])
        return next(gen, None)


class Solution3:
    """核心方法 - 对撞指针.

    对撞指针的想法源自于数组排序只需要 O(logN), 而最基本的解法需要 O(N^2), 因而进一步的思考有序数组
    的解法. 在对撞指针中, 发现每一次指针的移动, 都等价于抛弃了一个元素 (具体看下例). 对撞指针的关键在
    于当指针移动后, 当前元素将再也无法被选中, 因此要确保当前元素已经失去了价值.

    例如:
        数组为: [0, 3, 15, 26, 78, 99], 假设找 100. 将左右指针分别指向 0 和 99.

        因为 0 + 99 < 100, 所以 0 + 其他小于 99 的数都必定 < 100, 因此 0 没用了, 左指针向右移动.
        因为 3 + 99 > 100, 所以 其他大于 3 的数 + 99 都必定 > 100, 因此 99 没用了, 右指针向左移动.
        因为 3 + 78 < 100, 类推, 因此 3 没用了, 左指针向右移动.
        因为 15 + 78 < 100, 类推, 因此 15 没用了, 左指针向右移动.
        因为 26 + 78 != 100, 所以本题无解.
    """

    @staticmethod
    def twoSum(nums: List[int], target: int) -> Optional[List[int]]:
        # 使用 `enumerate` 保留原本的索引信息.
        # `nums` 使用类型的原因是 Pycharm 迷之识别不了 `enumerate` 的类型 ...
        nums: List[Tuple[int, int]] = list(enumerate(nums))
        nums.sort(key=itemgetter(1))
        l, r = 0, len(nums) - 1
        while l < r:
            total = nums[l][1] + nums[r][1]
            if total == target:
                return [nums[l][0], nums[r][0]]
            elif total < target:
                l += 1
            else:
                r -= 1
