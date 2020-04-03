import pytest

from structure import LinkedListV1, LinkedListV2


@pytest.mark.parametrize('cls', (LinkedListV1,
                                 LinkedListV2,))
def test_stack_related(cls):
    """测试链表中和栈相关的方法."""
    stack = cls()

    # 空栈不能 pop.
    assert list(stack) == []
    assert len(stack) == 0
    with pytest.raises(IndexError):
        stack.popleft()

    # 入 1 个出 1 个.
    stack.appendleft(10)
    assert list(stack) == [10]
    assert len(stack) == 1
    assert 10 == stack.popleft()
    assert list(stack) == []
    assert len(stack) == 0

    # 入 4 个出 2 个.
    for i in range(4):
        stack.appendleft(i)
    assert list(stack) == [3, 2, 1, 0]
    assert len(stack) == 4
    assert 3 == stack.popleft()
    assert 2 == stack.popleft()
    assert list(stack) == [1, 0]
    assert len(stack) == 2


def test_LinkedListV2():
    """测试 `LinkedListV2` 关于队列相关的方法.

    1. `append` 两个元素, 观察所有元素, `popleft` 两个元素后, 观察所有元素.
    2. `append` 一个元素, 观察所有元素, `popleft` 此元素.
        这一条主要是测试 `tail` 是否在只有一个元素的情况下 `popleft` 之后被重置了.
    3. `appendleft` 一个元素, 再 `append` 一个元素, 查看所有元素.
        这一条注意是测试 `tail` 是否在空的情况下 `appendleft` 之后移动了.
    """
    l = LinkedListV2()

    # 1
    l.append(0)
    l.append(1)
    assert list(l) == [0, 1]
    assert 0 == l.popleft()
    assert 1 == l.popleft()
    assert list(l) == []

    # 2
    l.append(2)
    assert list(l) == [2]
    l.popleft()

    # 3
    l.appendleft('c')
    l.append(10)
    assert list(l) == ['c', 10]
