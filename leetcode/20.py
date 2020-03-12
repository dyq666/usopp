class Solution:
    """核心方法 - Stack.

    当需要获取某个最近的数据时就需要使用栈.

    例如本题中当读到一个右括号时, 就需要获取最近的一个左括号.
    """

    brackets = {
        '(': ')',
        '{': '}',
        '[': ']',
    }

    @classmethod
    def isValid(cls, s: str) -> bool:
        letfs = []
        for c in s:
            if c in cls.brackets:
                letfs.append(c)
            else:  # 题目中说明了只有六种字符, 因此这里等价于 elif c in self.brackets.values()
                if not letfs or cls.brackets[letfs.pop()] != c:
                    return False
        # 题目中说明了空字符返回 True
        return not letfs


if __name__ == '__main__':
    f = Solution.isValid

    # 只有左括号或只有右括号
    assert not f(')}]')
    assert not f('({[')
    # 多了一个左括号或右括号
    assert not f('{{}}}')
    assert not f('{{{}}')
    # 正常
    assert f('{[()]}')
