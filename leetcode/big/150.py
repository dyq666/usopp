import operator
from typing import List

import pytest


class Solution:

    operator = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        # `operator.truediv` & `operator.floordiv` are not correct
        '/': lambda x, y: int(x / y)
    }

    def evalRPN(self, tokens: List[str]) -> int:
        values = []

        for token in tokens:
            if token in self.operator:
                right, left = values.pop(), values.pop()
                values.append(self.operator[token](left, right))
            else:
                values.append(int(token))

        return values.pop()


solution = Solution()


@pytest.mark.parametrize(('tokens', 'result'), (
    (['4', '13', '5', '/', '+'], 6),
    (['-10', '6', '+', '5', '/'], 0),
    (['-1', '5', '*', '4', '/'], -1)
))
def test_solution(tokens: List[str], result: int):
    assert solution.evalRPN(tokens) == result
