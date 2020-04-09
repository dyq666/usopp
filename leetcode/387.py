class Solution:
    """
    通常在用哈希表实现字典时, 需要在哈希表中存储 key 和 value,
    但这里实现的 hash_dict 实际上是一个无冲突的哈希表, 甚至可以
    根据索引反推出 key, 因而只需要存储 value (即, 题目中需要的频率).

    如果满足以下条件, 那么就可以实现一个无冲突的哈希表:
      - 元素种类确定 (这里是只有小写字母)
      - 种类数量比较小 (这里是只有 26 种)
    """

    def firstUniqChar(self, s: str) -> int:
        if not s:
            return -1

        hash_dict = [0 for _ in range(26)]
        hash_f = lambda o: ord(o) - ord('a')

        # 统计出现频率
        for c in s:
            hash_dict[hash_f(c)] += 1

        # 找到第一个出现频次是 1 的字符
        gen = (i for i, c in enumerate(s) if hash_dict[hash_f(c)] == 1)
        return next(gen, -1)


def test_solution():
    f = Solution().firstUniqChar

    # 空
    assert f('') == -1

    # 每个元素都重复
    assert f('abccba') == -1

    assert f('aabccd') == 2
