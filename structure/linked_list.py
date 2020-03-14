__all__ = (
    'LinkedListV1',
)

from typing import Any, Iterable, Optional

from .util import not_empty


class ListNode:

    def __init__(self, val: Any, next_: Optional['ListNode'] = None):
        self.val = val
        self.next = next_


class LinkedListV1:
    """单指针链表.

    `self._head` 其实是 -1 索引.
    """

    def __init__(self):
        self._head = ListNode(None)
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterable:
        needle = self._head
        for _ in range(self._size):
            needle = needle.next
            yield needle.val

    def appendleft(self, value: Any):
        self._head.next = ListNode(value, self._head.next)
        self._size += 1

    @not_empty
    def popleft(self) -> Any:
        res = self._head.next.val
        self._head.next = self._head.next.next
        self._size -= 1
        return res
