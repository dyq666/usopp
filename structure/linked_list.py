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

    只实现了两个 O(1) 的函数 `appendleft` 和 `popleft`, 可用于实现栈.
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

    在 V1 的基础上增加了 `append`, 但 `pop` 方式在单向链表中不好实现,
    因为在 `tail` 位置 `pop` 之后, `tail` 指针无法向前移动.

    `self._head` 其实相当于数组中的 -1 索引, `self._tail` 相当于 `len - 1`.
    也就是两个指针相对于动态数组都向前移动了一位, 原因是在链表中想要操作 index 位置
    的元素, 通常需要找到 index - 1 位置的元素.

    需要注意的是当链表中只有一个元素并且执行 `popleft` 后需要重置 `tail`.
    重置前的 `tail` 实际上指向被 `popleft` 出去的元素. 而当空链表 `appendleft`
    一个元素后需要移动 `tail`. 另外从这里也看出使用 dummy_head 的好处, `head`
    永远指向 dummy_head, 不需要像 `tail` 一样处理特殊的情况.

    另外数据结构中关于栈相关的属性可以去 LeetCode 20 上测试.
    """

    def __init__(self):
        self._head = Node(None)
        self._tail = self._head
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator:
        # 相当于从索引为 0 的位置开始
        needle = self._head.next
        for _ in range(self._size):
            yield needle.val
            needle = needle.next

    def append(self, value: Any):
        self._tail.next = Node(value, self._tail.next)
        self._tail = self._tail.next
        self._size += 1

    def appendleft(self, value: Any):
        self._head.next = Node(value, self._head.next)
        self._size += 1

        if len(self) == 1:
            self._tail = self._head.next

    @not_empty
    def popleft(self) -> Any:
        res = self._head.next
        self._head.next = res.next
        res.next = None
        self._size -= 1

        if len(self) == 0:
            self._tail = self._head

        return res.val


class LinkedListV3:

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
    def append_left(self, val: Any):
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
