import pytest

from structure import LinkedListV1, LinkedListV2


class TestLinkedListV1:

    def test_empty(self):
        l = LinkedListV1()

        # 初始情况
        assert len(l) == 0
        assert list(l) == []
        assert l._head is None

    def test_append_left(self):
        l = LinkedListV1()

        # 在头指针添加元素, 因为插入的是链表中第一个元素, 所以尾指针也移动了
        l.appendleft(1)
        assert len(l) == 1
        assert list(l) == [1]
        assert l._head.val == 1

    def test_popleft(self):
        l = LinkedListV1.from_iterable([1])

        # 在头指针弹出元素
        assert 1 == l.popleft()
        assert len(l) == 0
        assert list(l) == []
        assert l._head is None

        # 空链表不能弹出元素
        with pytest.raises(IndexError):
            l.popleft()


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
