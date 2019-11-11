from collections import namedtuple

import pytest

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


def test_min_stack():
    min_stack = MinStack()
    min_stack.push(10)
    min_stack.push(-2)
    min_stack.push(-1)

    assert min_stack._stack == [
        StackItem(10, 10),
        StackItem(-2, -2),
        StackItem(-1, -2)
    ]
    assert min_stack.getMin() == -2
    assert min_stack.top() == -1

    min_stack.pop()
    min_stack.pop()
    assert min_stack.getMin() == 10

    min_stack.pop()
    assert min_stack._stack == []
    with pytest.raises(IndexError):
        min_stack.getMin()
