from itertools import combinations_with_replacement


class Solution:
    """核心方法 - 组合.

    子串实际上等于两个索引之间的字符串, 因此求所有子串就是求所有索引对.
    而索引对之间排列是等价的, 因而这个问题变成了一个组合问题.

    此外时间复杂度是 O(N^3), len(str_) == len(set(str_)) 也是很耗时的.
    具体计算方法参考: https://leetcode.com/articles/longest-substring-without-repeating-characters/
    """

    @staticmethod
    def lengthOfLongestSubstring(s: str) -> int:
        sub_strs = (s[i:j + 1] for i, j in combinations_with_replacement(range(len(s)), 2))
        max_length = (len(set(str_)) for str_ in sub_strs if len(str_) == len(set(str_)))
        return max(max_length, default=0)


class Solution2:
    """核心方法 - 滑动窗口.

    这里提供一种通用的滑动窗口解法:
      - 假定窗口的范围是左闭右开的, 即 [l, r).
      - 让窗口在开始和结束时都为空, 也就是 [0, 0) 和 [len, len). (即 l 和 r 初始值为 0, 终止值为 len).
        因为 l <= r 永远成立, 因此我们只需要确保 l 终止于 len. 因而 while 循环的条件是 l < len, 相当于
        最后一次循环会将 l 从 len - 1 推到 len.
      - 因为 r 会想到达 len, 所以必须在推动 r 时, 需要确保 r 未到 len.

    滑动窗口时间复杂度为 O(N), 实际上就是 l 和 r 分别执行了一次遍历.

    对于本题来说, 当下一个元素 (即, s[r]) 在窗口内则左移, 否则右移.

    此外, 对于本题来说求得是最大的窗口长度, 因此只需使 r 到达 len 即可. (lengthOfLongestSubstring2)

    lengthOfLongestSubstring3 做了一小步优化, 当下一个元素在窗口内时, 直接找到 l 下一步的位置, 而不是
    一步一步的向前移动.
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

    @staticmethod
    def lengthOfLongestSubstring3(s: str) -> int:
        chars = set()
        max_len = 0
        l, r = 0, 0

        while r < len(s):
            if s[r] not in chars:
                chars.add(s[r])
                r += 1
                max_len = max(max_len, r - l)
            else:
                next_index = s.index(s[r], l) + 1
                for c in s[l: next_index]:
                    chars.remove(c)
                l = next_index
        return max_len
