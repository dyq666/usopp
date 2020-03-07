class Solution:
    """核心方法 - 滑动窗口.

    这里提供一种通用的滑动窗口解法:
      - 假定窗口的范围是左闭右开的, 即 [l, r).
      - 让窗口在开始和结束时都为空, 也就是 [0, 0) 和 [len, len). (即 l 和 r 初始值为 0, 终止值为 len).
        因为 l <= r 永远成立, 因此我们只需要确保 l 终止于 len. 因而 while 循环的条件是 l < len, 相当于
        最后一次循环会将 l 从 len - 1 推到 len.
      - 因为 r 会想到达 len, 所以必须在推动 r 时, 需要确保 r 未到 len.

    滑动窗口时间复杂度为 O(N), 实际上就是 l 和 r 分别执行了一次遍历.

    此外, 对于本题来说求得是最大的窗口长度, 因此只需使 r 到达 len 即可. (lengthOfLongestSubstring2)
    """

    @staticmethod
    def lengthOfLongestSubstring(s: str) -> int:
        chars = set()
        max_len = 0
        l, r = 0, 0

        while l < len(s):
            if r < len(s) and s[r] not in chars:
                chars.add(s[r])
                r += 1
                max_len = max(max_len, r - l)
            else:
                chars.remove(s[l])
                l += 1
        return max_len

    @staticmethod
    def lengthOfLongestSubstring2(s: str) -> int:
        chars = set()
        max_len = 0
        l, r = 0, 0

        while r < len(s):
            if s[r] not in chars:
                chars.add(s[r])
                r += 1
                max_len = max(max_len, r - l)
            else:
                chars.remove(s[l])
                l += 1
        return max_len
