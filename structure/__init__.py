from typing import Any, Iterable, Optional


class DynamicArray:
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
    """

    MIN_SIZE = 10

    def __init__(self):
        self._data = [None for _ in range(self.MIN_SIZE)]
        self._size = 0

    def __len__(self):
        return self._size

    def __repr__(self) -> str:
        return repr(self._data)

    def __iter__(self) -> Iterable:
        return iter(self._data[:self._size])

    def __contains__(self, value: Any) -> bool:
        return value in self._data[:self._size]

    def __getitem__(self, index: int) -> Any:
        if not (0 <= index < self._size):
            raise IndexError
        return self._data[index]

    def __setitem__(self, index: int, value: Any):
        if not (0 <= index < self._size):
            raise IndexError
        self._data[index] = value

    def insert(self, value: Any, index: Optional[int] = None):
        """插入元素.

        如果不传 `index` 则向末尾插入.
        """
        index = self._size if index is None else index

        if not (0 <= index <= self._size):
            raise IndexError

        if self._size == len(self._data):
            self._resize(len(self._data) * 2)

        self._data[index + 1: self._size + 1] = self._data[index: self._size]
        self._data[index] = value
        self._size += 1

    def pop(self, index: Optional[int] = None) -> Any:
        """删除元素.

        如果不传 `index` 则从末尾删除.
        """
        index = self._size - 1 if index is None else index

        if not (0 <= index < self._size):
            raise IndexError

        if self._size == len(self._data) // 4:
            self._resize(len(self._data) // 2)

        res = self._data[index]
        self._data[index: self._size - 1] = self._data[index + 1: self._size]
        self._size -= 1
        return res

    def _resize(self, capacity: int):
        """改变静态数组的容量."""
        # 永久使 capacity >= 10
        if capacity < self.MIN_SIZE:
            return
        old = self._data
        self._data = [None for _ in range(capacity)]
        self._data[:self._size] = old[:self._size]
