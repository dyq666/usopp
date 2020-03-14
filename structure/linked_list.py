__all__ = (
    'LinkedListV1',
    'LinkedListV2',
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

    只实现了两个 O(1) 的 `appendleft` 和 `popleft`.

    另外数据结构中关于栈相关的属性可以去 LeetCode 20 上测试.
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


class LinkedListV2:
    """双指针链表.

    在 V1 的基础上增加了 `append`, 但 `pop` 方式只靠两个指针还无法实现,
    因为在 `tail` 位置 `pop` 之后, `tail` 无法找到前一个元素.

    此外需要注意的是当链表中只有一个元素并且执行 `popleft` 后需要重置 `tail`.
    重置前的 `tail` 实际上指向被 `popleft` 出去的元素.

    另外数据结构中关于栈相关的属性可以去 LeetCode 20 上测试.
    """

    def __init__(self):
        self._head = ListNode(None)
        self._tail = self._head
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterable:
        needle = self._head
        for _ in range(self._size):
            needle = needle.next
            yield needle.val

    def append(self, value: Any):
        self._tail.next = ListNode(value, self._tail.next)
        self._tail = self._tail.next
        self._size += 1

    def appendleft(self, value: Any):
        self._head.next = ListNode(value, self._head.next)
        self._size += 1

    @not_empty
    def popleft(self) -> Any:
        res = self._head.next.val
        self._head.next = self._head.next.next
        self._size -= 1

        if len(self) == 0:
            self._tail = self._head

        return res
