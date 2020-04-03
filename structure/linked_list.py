__all__ = (
    'LinkedListV1',
    'LinkedListV2',
)

from typing import Any, Iterable, Iterator, Optional

from .util import not_empty, size_change


class Node:

    def __init__(self, val: Any, next_: Optional['Node'] = None):
        self.val = val
        self.next = next_


class LinkedListV1:
    """头指针单向链表.

    只实现了两个 O(1) 的函数 `appendleft popleft`, 可用于实现栈.
    """

    def __init__(self):
        self._head: Optional[Node] = None
        self._size = 0

    def __iter__(self) -> Iterator:
        cur = self._head
        while cur:
            yield cur.val
            cur = cur.next

    def __len__(self) -> int:
        return self._size

    @size_change(1)
    def appendleft(self, value: Any):
        self._head = Node(value, self._head)

    @not_empty
    @size_change(-1)
    def popleft(self) -> Any:
        poped_val = self._head.val
        self._head = self._head.next
        return poped_val


class LinkedListV2:
    """头尾指针单向链表.

    只实现了三个 O(1) 的函数 `append appendleft popleft`, 可用于实现栈, 队列.
    """

    def __init__(self):
        self._size = 0
        self._head = None
        self._tail = None

    def __len__(self) -> int:
        return self._size

    @size_change(1)
    def append(self, val: Any):
        """在尾指针添加元素."""
        # 因为插入的是链表中第一个元素, 所以头指针也要移动
        if len(self) == 0:
            self._head = self._tail = Node(val)
            return

        self._tail.next = Node(val)
        self._tail = self._tail.next

    @size_change(1)
    def appendleft(self, val: Any):
        """在头指针添加元素."""
        # 因为插入的是链表中第一个元素, 所以尾指针也要移动
        if len(self) == 0:
            self._tail = self._head = Node(val)
            return

        self._head = Node(val, self._head)

    @size_change(-1)
    def popleft(self) -> Any:
        """在头指针弹出元素."""
        poped_val = self._head.val

        # 因为弹出的是链表中最后一个元素, 所以尾指针也要指向 None
        if len(self) == 1:
            self._tail = self._head = None
        else:
            self._head = self._head.next

        return poped_val

    @classmethod
    def from_iterable(cls, vals: Iterable):
        l = cls()
        for val in vals:
            l.append(val)
        return l
