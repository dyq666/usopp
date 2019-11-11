# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/29 16:55'


class Solution:
    def findAnagrams(self, s, p):
        """
        1. 辅助变量：target_counter存放p，cur_dict存放当前符合条件的字符。
        2. 移动条件：滑动窗口的长度小于目标长度，右边界右移动，否则左边界右移。
        3. 改变结果：target_counter与cur_dict一样，则记录当前left。
        4. 返回结果：结果为所有符合条件的窗口的左边界索引
        """
        from collections import Counter

        left, right = 0, -1

        target_counter, target_len = Counter(p), len(p)
        cur_dict = {}

        found_indexes = []

        while left < len(s):

            if right + 1 < len(s) and right - left + 1 < target_len:
                cur_dict[s[right + 1]] = cur_dict.setdefault(s[right + 1], 0) + 1
                right += 1

            else:
                cur_dict[s[left]] -= 1
                if cur_dict[s[left]] == 0:
                    cur_dict.pop(s[left])

                left += 1

            if right - left + 1 == target_len and target_counter == cur_dict:
                found_indexes.append(left)

        return found_indexes
