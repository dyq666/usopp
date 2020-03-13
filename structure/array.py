__all__ = (
    'DynamicArrayV1',
    'DynamicArrayV2',
    'LoopArray',
)

from functools import wraps
from typing import Any, Callable, Iterable


def check_index(offset: int = 0) -> Callable:
    """在执行数据结构某个方法前检查索引是否有效.

    方法必须满足第一个参数是 `self`, 第二是索引, 同时类必须实现 `__len__`.

    索引的检查范围是 [0, len + offset).
    """
    def deco(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(self: Any, index: int, *args, **kwargs):
            if not (0 <= index < len(self) + offset):
                raise IndexError
            return f(self, index, *args, **kwargs)

        return wrapper

    return deco


class DynamicArrayV1:
    """动态数组 V1.

    动态数组是在静态数组的基础上封装的. 在 Python 中, 没有常用的静态数组,
    在这里我们限制下 list 的功能, 使 list 只能在初始化时确定大小 (list 实际上就是动态数组).

    动态数组的核心内容:
      1. capacity (容量) 和 size. capacity 代表底层静态数组的大小, 而 size 代表动态数组的大小.
         二者满足 size <= capacity 且 capacity != 0 (在本类中限制 capacity >= 10).
      2. 扩容和缩容. 增加元素时如果 size == capacity (相当于静态数组满了), 就需要增大底层的静态数组.
         删除元素时如果 size == capacity / 4 (这里具体到容量的多少才缩容, 可以按需更改),
         就需要缩减底层的静态数组, 通常让缩减后的 capacity 仍大于 size. 例如在本类中,
         当 size == capacity / 4 时缩容, 将容积缩为 capactiy / 2, 此时 capacity == 2 * size,
         动态数组中仍有空间可以添加元素. 如果容积缩为 capacity / 4, 此时 capacity == size,
         添加元素就又需要扩容了, 消耗时间 (引起复杂度震荡).

    动态数组作为栈使用时, 只需要实现 `append` 和 `pop`, 因此在 V1 版本中只实现栈需要的功能.

    此外可以用 LeetCode 20 来测试本数据结构是否正确.
    """

    MIN_SIZE = 10

    def __init__(self):
        self._data = [None for _ in range(self.MIN_SIZE)]
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterable:
        return iter(self._data[:len(self)])

    def append(self, value: Any):
        # 扩容
        if len(self) == self._capacity:
            self._resize(2 * self._capacity)

        self._data[len(self)] = value
        self._size += 1

    def pop(self) -> Any:
        if len(self) == 0:
            raise IndexError

        res = self._data[len(self) - 1]
        # 让垃圾回收机制可以回收此处的元素
        self._data[len(self) - 1] = None
        self._size -= 1

        # 缩容
        if len(self) == self._capacity // 4:
            self._resize(self._capacity // 2)

        return res

    def _resize(self, capactiy: int):
        if capactiy < self.MIN_SIZE:
            return
        new = [None for _ in range(capactiy)]
        new[:len(self)] = self._data[:len(self)]
        self._data = new

    @property
    def _capacity(self) -> int:
        return len(self._data)


class DynamicArrayV2:
    """动态数组 V2.

    在 V1 的基础上提供了按任意索引插入或删除元素, 同时也提供了 get / set / contains.
    V2 和 V1 最大的区别就是插入和删除元素时, 需要用一个 O(N) 的操作移动数组中的元素.

    此外可以用 LeetCode 20 来测试本数据结构中栈相关的操作是否正确.
    """

    MIN_SIZE = 10

    def __init__(self):
        self._data = [None for _ in range(self.MIN_SIZE)]
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterable:
        return iter(self._data[:len(self)])

    @check_index()
    def __getitem__(self, index: int) -> Any:
        return self._data[index]

    @check_index()
    def __setitem__(self, index: int, value: Any):
        self._data[index] = value

    def __contains__(self, value: Any):
        return value in self._data[:len(self)]

    @check_index(offset=1)
    def insert(self, index: int, value: Any):
        # 扩容
        if len(self) == self._capacity:
            self._resize(2 * self._capacity)

        # [index, size) 向后移动一位
        self._data[index + 1: len(self) + 1] = self._data[index: len(self)]
        self._data[index] = value
        self._size += 1

    def append(self, value: Any):
        self.insert(len(self), value)

    @check_index()
    def remove(self, index: int) -> Any:
        if not (0 <= index < len(self)):
            raise IndexError

        res = self._data[index]
        # [index + 1, len) 向前移动一位
        self._data[index: len(self) - 1] = self._data[index + 1: len(self)]
        # 让垃圾回收机制可以回收此处的元素
        self._data[len(self) - 1] = None
        self._size -= 1

        # 缩容
        if len(self) == self._capacity // 4:
            self._resize(self._capacity // 2)

        return res

    def pop(self) -> Any:
        return self.remove(len(self) - 1)

    def _resize(self, capacity: int):
        if capacity < self.MIN_SIZE:
            return
        new = [None for _ in range(capacity)]
        new[:len(self)] = self._data[:len(self)]
        self._data = new

    @property
    def _capacity(self) -> int:
        return len(self._data)


class LoopArray:
    """头尾指针数组.

    头尾指针数组实际上是动态数组到循环数组的过渡. 头尾指针数组头插入的时间复杂度为 O(1),
    而不是动态数组的 O(N), 但同时引入了空间浪费的问题, 这个问题需要由循环数组解决.

    这里偷了个懒, 目前只实现了头出尾进的功能, 不提供其他位置的插入或删除.

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
