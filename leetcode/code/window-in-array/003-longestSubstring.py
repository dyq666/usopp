# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/29 16:49'


class Solution:

    def lengthOfLongestSubstring(self, s):
        """
        1. 滑动窗口：左闭右闭。初始值-[0, -1]。
        2. 辅助变量：
            （1）符合条件的滑动窗口最长长度，初始值0。
        3. 终止条件：左边界推到末端，右边界也推到末端。但是右边界会比左边界先推到末端，所以判断中只需要判断左边界即可。
        4. 移动条件：窗口右边的值是否在窗口中，是左边界右移动，不是右边界右移动。
        5. 改变结果：当前的滑动窗口是最大长度。
        6. 返回值：窗口最大长度
        """
        left, right = 0, -1  # [left...right]

        max_len = 0

        # 终止条件
        while left < len(s):

            if right + 1 < len(s) and s[right + 1] not in s[left:right + 1]:
                right += 1
            else:
                left += 1

            max_len = max(max_len, right - left + 1)

        return max_len

    def lengthOfLongestSubstring02(self, s):
        """
        1. 优化(一): 用set代替字符串的查询
        """
        left, right = 0, -1  # [left...right]

        max_len = 0

        # 优化一
        window_ele = set()

        while left < len(s):

            if right + 1 < len(s) and s[right + 1] not in window_ele:
                window_ele.add(s[right + 1])
                right += 1
            else:
                window_ele.remove(s[left])
                left += 1

            max_len = max(max_len, right - left + 1)

        return max_len

    def lengthOfLongestSubstring03(self, s):
        """
        1. 优化：直接找到重复的位置
        """
        left, right = 0, -1  # [left...right]

        max_len = 0

        while left < len(s):
            if right + 1 >= len(s):
                break

            search = s.find(s[right + 1], left, right + 1)

            if search == -1:
                right += 1
            else:
                left = search + 1

            max_len = max(max_len, right - left + 1)

        return max_len
