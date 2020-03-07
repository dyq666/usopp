class Solution:

    @staticmethod
    def lengthOfLongestSubstring(s: str) -> int:
        """核心方法 - 滑动窗口.

        窗口的范围是左闭右开的, 因此 l ∈ [0, len(s)), r ∈ [0, len(s)].

        - 窗口停止滑动的条件: 当 r 等于 len(s) 时窗口就不能向右滑动了, 所以窗口的滑动条件是 r < len(s).
        - 窗口左滑右滑的条件: 当窗口右侧的第一个元素的值在窗口内, 则左移. 相反则右移.
        """
        chars = set()
        max_len = 0
        l, r = 0, 0

        while r < len(s):
            next_value = s[r]
            if next_value in chars:
                chars.remove(s[l])
                l += 1
            else:
                chars.add(next_value)
                r += 1
                max_len = max(max_len, r - l)
        return max_len
