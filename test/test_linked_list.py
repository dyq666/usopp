import pytest

from structure import LinkedListV1, LinkedListV2


@pytest.mark.parametrize('cls', (LinkedListV1, LinkedListV2))
def test_LinkedListV1_and_part_of_LinkedListV2(cls):
    """测试 `LinkedList` 的所有方法和 `LinkedListV2` 用于栈相关的操作.

    1. 初始状态, 查看所有元素, 无法 `popleft`.
    2. `appendleft` 四个元素, 查看所有元素. 再 `popleft` 两个元素, 查看所有元素.
    """
    l = cls()

    # 1
    assert list(l) == []
    with pytest.raises(IndexError):
        l.popleft()

    # 2
    for i in range(3, -1, -1):
        l.appendleft(i)
    assert list(l) == list(range(4))
    for i in range(2):
        assert i == l.popleft()
    assert list(l) == [2, 3]


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
