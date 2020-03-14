import pytest

from structure import LinkedListV1


def test_LinkedListV1():
    """测试 `LinkedList` 的所有方法.

    1. 初始状态, 查看所有元素, 无法 `popleft`.
    2. `appendleft` 四个元素, 查看所有元素. 再 `popleft` 两个元素, 查看所有元素.
    """
    l = LinkedListV1()

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
