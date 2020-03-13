__all__ = (
    'DynamicArrayV2',
    'TwoPointsArray',
)

from typing import Any, Iterable, Optional


class DynamicArray:
    pass


class DynamicArrayV2:
    """动态数组.

    动态数组是在静态数组的基础上封装的. 在 Python 中, 没有常用的静态数组,
    在这里我们限制下 list 的功能, 让它扮演静态数组的角色 (list 实际上就是动态数组).

    动态数组的核心有两个:
      1. capacity (容量) 和 size. capacity 代表底层静态数组的大小, 而 size 代表动态数组的大小.
         二者满足 size <= capacity 且 capacity != 0 (在本类中限制 capacity >= 10).
      2. 扩容和缩容. 增加元素时如果 size == capacity (相当于静态数组满了), 就需要增大底层的静态数组.
         删除元素时如果 size == capacity / 4 (这里具体到容量的多少才缩容, 可以按需更改),
         就需要缩减底层的静态数组, 通常让缩减后的 capacity 仍大于 size. 例如在本类中,
         当 size == capacity / 4 时缩容, 将容积缩为 capactiy / 2, 此时 capacity == 2 * size,
         动态数组中仍有空间可以添加元素. 如果容积缩为 capacity / 4, 此时 capacity == size,
         添加元素就又需要扩容了, 消耗时间.

    此外可以用 LeetCode 20 来测试本数据结构是否正确.
    """

    MIN_SIZE = 10

    def __init__(self):
        self._data = [None for _ in range(self.MIN_SIZE)]
        self._size = 0

    def __len__(self):
        return self._size

    def __repr__(self) -> str:
        return repr(self._data[:len(self)])

    def __getitem__(self, index: int) -> Any:
        if not (0 <= index < len(self)):
            raise IndexError
        return self._data[index]

    def __setitem__(self, index: int, value: Any):
        if not (0 <= index < len(self)):
            raise IndexError
        self._data[index] = value

    def insert(self, value: Any, index: Optional[int] = None):
        """插入元素.

        如果不传 `index` 则向末尾插入.
        """
        index = len(self) if index is None else index

        if not (0 <= index < len(self) + 1):
            raise IndexError

        # 扩容
        if len(self) == len(self._data):
            self._resize(len(self._data) * 2)

        self._data[index + 1: len(self) + 1] = self._data[index: len(self)]
        self._data[index] = value
        self._size += 1

    def pop(self, index: Optional[int] = None) -> Any:
        """删除元素.

        如果不传 `index` 则从末尾删除.
        """
        index = len(self) - 1 if index is None else index

        if not (0 <= index < len(self)):
            raise IndexError

        res = self._data[index]
        self._data[index: len(self) - 1] = self._data[index + 1: len(self)]
        self._size -= 1
        # `len(self)` 的元素实际上不会被动态数组访问, 如果不将此元素改为 None
        # 的话, 此处的对象会一直存在静态数组中, 因而不会被垃圾回收机制回收, 占用内存.
        self._data[len(self)] = None

        # 缩容
        if len(self) == len(self._data) // 4:
            self._resize(len(self._data) // 2)

        return res

    def _resize(self, capacity: int):
        """改变静态数组的容量."""
        if capacity < self.MIN_SIZE:
            return
        new = [None for _ in range(capacity)]
        new[:len(self)] = self._data[:len(self)]
        self._data = new


class TwoPointsArray:
    """头尾指针数组.

    这里只实现了头出尾进的功能 (因此可能叫队列更加准确).

    此数据结构的缺陷是:
      1. 数组中的 `head` 和 `tail` 只能向右移动, 导致部分空间被浪费.
      2. 扩容和缩容都是根据 `tail` 来决定的, 而不是根据 `len`
         决定 (因为只能向右移动, 所以必须用 `tail`), 导致会频繁的触发
         `_resize` 使 `append`, `popleft` 并不一定是 O(1) 的
         时间复杂度了 (也叫做复杂度震荡).
    """

    MIN_SIZE = 10

    def __init__(self):
        self._data = [None for _ in range(self.MIN_SIZE)]
        self._tail = 0
        self._head = 0

    def __len__(self) -> int:
        return self._tail - self._head

    def __repr__(self) -> str:
        return repr(self._data[self._head:self._tail])

    def __getitem__(self, index: int) -> Any:
        if not (self._head <= index < self._tail):
            raise IndexError
        return self._data[index]

    def __iter__(self) -> Iterable:
        return iter(self._data[self._head:self._tail])

    def append(self, value: Any):
        # 扩容
        if self._tail == self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._tail] = value
        self._tail += 1

    def popleft(self) -> Any:
        if len(self) == 0:
            raise IndexError

        res = self._data[self._head]
        # 让垃圾回收可以回收此处的元素.
        self._data[self._head] = None
        self._head += 1

        # 缩容
        if self._tail <= self._capacity // 4:
            self._resize(self._capacity // 2)

        return res

    def _resize(self, capacity: int):
        if capacity < self.MIN_SIZE:
            return
        new = [None for _ in range(capacity)]
        new[:len(self)] = self._data[self._head:self._tail]
        # 这里必须用 tuple unpack, 因为 `len(self)` 的计算跟 `self._head` 有关
        self._head, self._tail = 0, len(self)
        self._data = new

    @property
    def _capacity(self):
        return len(self._data)
