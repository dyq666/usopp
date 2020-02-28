class Solution:

    def twoSum02(self, nums, target):
        """
        1. O(nlogn)-快排
        2. 使用双指针
        3. 从题目中的得知每个target只有一个答案, 意味着如果target是6
           不会出现[2, 2, 4]的情况, 但是会出现[3, 3]的情况, 也就是当
           两个相同的值满足情况是才会有重复的元素
        """
        raw_nums = nums

        nums = sorted(nums)

        left, right = 0, len(nums) - 1

        while left < right:
            v_left, v_right = nums[left], nums[right]

            two_sum = v_left + v_right

            if two_sum > target:
                right -= 1
            elif two_sum < target:
                left += 1
            else:  # 找到了
                left_index = raw_nums.index(v_left)
                # 如果值相同就查找下一个该值的索引
                right_index = raw_nums.index(v_right, left + 1) if v_right == v_left else raw_nums.index(v_right)
                return [left_index, right_index]
