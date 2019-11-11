## 概述

代码地址: <https://github.com/dyq666/leetcode_for_python/tree/master/stack>

两种栈的使用场景:

- 获取最近的某种数据
- 出栈时恢复原有的环境

##  获取最近的某种数据

### 20 有效括号

[原题链接](<https://leetcode.com/problems/valid-parentheses/>)

#### 已知条件:

- 字符串中的字符仅有 `{}` `[]` `()` 6 种

- 空字符串是有效的

#### 解题思路:

使用栈的原因:

遍历字符串遇到右括号时, 需要知道最近的左括号, 或者说之前遍历中最后一次出现的左括号. 才能判断左右括号是否匹配 (即, 需要栈后入先出的特性)

具体的步骤:

1. 如果是空字符串, 返回 `True`
2. 遍历字符串, 如果是左括号就入栈, 如果是右括号就判断是否匹配. 匹配的条件是栈不为空且栈顶的左括号和右括号是一对. 如果匹配失败则返回 `Fasle`

3. 遍历结束后意味着所有右括号都成功的匹配了, 但是可能还有剩余的左括号, 因此需要判断栈是否为空.

```python
class Solution:

    brackets = {
        '{': '}',
        '[': ']',
        '(': ')'
    }

    def isValid(self, s: str) -> bool:
        # 步骤 1
        if not s:
            return True
		
        # 步骤 2
        left = []
        for c in s:
            if c in self.brackets:
                left.append(c)
            elif not left or not self.brackets[left.pop()] == c:
                return False

        # 步骤 3
        return not left
```

#### 其他相关题目:

[71 简化 Unix 路径](<https://leetcode.com/problems/simplify-path/>), 每次遇到 `..` 需要删除最近的路径

[150 计算反向逆波兰表达式](<https://leetcode.com/problems/evaluate-reverse-polish-notation/>), 每次遇到 `+ - * /` 需要最近的两个数

## 出栈时恢复原有的环境

### 155 最小栈

[原题链接](<https://leetcode.com/problems/min-stack/>)

#### 已知条件:

- 所有测试操作都是有效的, 例如 `pop` 前不需要判断是否为空. (真实情况下需要解决为空的情况)

#### 解题思路:

栈通常情况只会存储一个简单的值. 但是本题需要存值和当前的最小值的 `tuple`. 这样无论进行多少次出栈 or 入栈操作都能用 `O(1)` 的时间复杂度获取最小值.

不论是最小值, 最大值还是平均值都可以理解为入栈时刻的环境, 入栈时将环境也存储下来, 那么需要时就可以直接使用环境. 这是一种通过空间换取时间的做法.

```python
from collections import namedtuple

StackItem = namedtuple('StackItem', 'value min')


class MinStack:

    def __init__(self):
        self._stack = []

    def push(self, x: int) -> None:
        min_ = min(x, self.getMin()) if self._stack else x
        self._stack.append(StackItem(x, min_))

    def pop(self) -> None:
        self._stack.pop()

    def top(self) -> int:
        return self._stack[-1].value

    def getMin(self) -> int:
        return self._stack[-1].min
```

