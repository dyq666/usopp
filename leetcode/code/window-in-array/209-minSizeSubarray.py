class Solution:
    def minSubArrayLen(self, s, nums):
        """
        1. 滑动窗口：左闭右闭。初始值-[0, -1]。
        2. 辅助变量：（1）滑动窗口中的sum，初始值为0。
                    （2）符合条件的滑动窗口的最小值，初始值None，如果遍历完了还是None则返回0。
        3. 终止条件：左边界推到末端，右边界也推到末端。但是右边界会比左边界先推到末端，所以判断中只需要判断左边界即可。
        4. 滑动条件：滑动窗口中的sum小于s，则右边界右移，否则左边界右移动。
        5. 改变结果：滑动窗口中的sum大于等于s，并且当前的滑动窗口是最短长度。
        6. 返回结果：如果还是None则返回0
        """
        # 滑动窗口范围
        l, r = 0, -1

        # 辅助变量
        window_sum = 0
        min_len = None

        # 终止条件
        while l < len(nums):

            # 滑动条件
            if window_sum < s and r + 1 < len(nums):
                window_sum += nums[r + 1]
                r += 1
            else:
                window_sum -= nums[l]
                l += 1

            # 改变结果
            if window_sum >= s:
                min_len = min(min_len, r - l + 1) if min_len is not None else r - l + 1
        # 返回结果
        return min_len if min_len is not None else 0
