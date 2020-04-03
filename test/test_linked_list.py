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


class TestLinkedListV2:

    def test_empty(self):
        l = LinkedListV2()

        # 初始情况
        assert len(l) == 0
        assert list(l) == []
        assert l._head is None
        assert l._tail is None

    def test_append(self):
        l = LinkedListV2()

        # 在尾指针添加元素, 因为插入的是链表中第一个元素, 所以头指针也移动了
        l.append(1)
        assert len(l) == 1
        assert list(l) == [1]
        assert l._head.val == 1
        assert l._tail.val == 1

        # 在尾指针插入第二个元素, 此时头指针不移动
        l.append(2)
        assert len(l) == 2
        assert list(l) == [1, 2]
        assert l._head.val == 1
        assert l._tail.val == 2

    def test_append_left(self):
        l = LinkedListV2()

        # 在头指针添加元素, 因为插入的是链表中第一个元素, 所以尾指针也移动了
        l.appendleft(1)
        assert len(l) == 1
        assert list(l) == [1]
        assert l._head.val == 1
        assert l._tail.val == 1

        # 在头指针插入第二个元素, 此时尾指针不移动
        l.appendleft(2)
        assert len(l) == 2
        assert list(l) == [2, 1]
        assert l._head.val == 2
        assert l._tail.val == 1

    def test_popleft(self):
        l = LinkedListV2.from_iterable([1, 2])

        # 在头指针弹出元素
        assert 1 == l.popleft()
        assert len(l) == 1
        assert list(l) == [2]
        assert l._head.val == 2
        assert l._tail.val == 2

        # 头指针弹出元素, 因为弹出的是链表中最后一个元素, 所以尾指针也要指向 None
        assert 2 == l.popleft()
        assert len(l) == 0
        assert list(l) == []
        assert l._head is None
        assert l._tail is None

        # 空链表不能弹出元素
        with pytest.raises(IndexError):
            l.popleft()
