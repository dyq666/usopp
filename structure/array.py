__all__ = (
    'DynamicArrayV1',
    'DynamicArrayV2',
    'LoopArrayV1',
    'LoopArrayV2',
    'LoopArrayV3',
)

from typing import Any, Iterator

from .util import check_index, not_empty


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

    def __iter__(self) -> Iterator:
        return iter(self._data[:len(self)])

    def append(self, value: Any):
        # 扩容
        if len(self) == self._capacity:
            self._resize(2 * self._capacity)

        self._data[len(self)] = value
        self._size += 1

    @not_empty
    def pop(self) -> Any:
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
        new[:len(self)] = list(self)
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

    def __iter__(self) -> Iterator:
        # __contains__ 实际上是不需要显示定义的, Python 会自动调用 __iter__,
        # 它的实现等价于 `return value in iter(self)`
        return iter(self._data[:len(self)])

    @check_index()
    def __getitem__(self, index: int) -> Any:
        return self._data[index]

    @check_index()
    def __setitem__(self, index: int, value: Any):
        self._data[index] = value

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
        new[:len(self)] = list(self)
        self._data = new

    @property
    def _capacity(self) -> int:
        return len(self._data)


class LoopArrayV1:
    """头尾指针数组.

    头尾指针数组实际上是动态数组到循环数组的过渡. 此数组相较于动态数组的优点是
    头插入的时间复杂度为 O(1), 但同时也引入了如下问题:

      1. 数组中的 `_head` 和 `_tail` 只能向右移动, 导致左部空间被浪费.
      2. 扩容和缩容都是根据 `_tail` 来决定的, 而不是根据 `len` (因为只能向右移动, 所以必须用 `_tail`),
         导致会频繁的触发 `_resize` 使 `append`, `popleft` 不再是 O(1) 的时间复杂度了 (产生了复杂度震荡).

    实际上循环数组中的 `_size` 和 `_tail` 是一样的, 而循环数组中的 `_tail` 永远等于 0.

    循环数组作为队列使用时, 只需要实现 `append` 和 `popleft`, 因此在 V1 版本中只实现这些功能.

    另外在本数据结构中, 由于底层静态数组非常容易被填充满, 因此不再进行缩容, 只进行扩容,
    扩容的大小应为实际动态数组的两倍.
    """

    MIN_SIZE = 10

    def __init__(self):
        self._data = [None for _ in range(self.MIN_SIZE)]
        self._tail = 0
        self._head = 0

    def __len__(self) -> int:
        return self._tail - self._head

    def __iter__(self) -> Iterator:
        return iter(self._data[self._head:self._tail])

    def append(self, value: Any):
        # 扩容
        if self._tail == self._capacity:
            self._resize(len(self) * 2)

        self._data[self._tail] = value
        self._tail += 1

    @not_empty
    def popleft(self) -> Any:
        res = self._data[self._head]
        # 让垃圾回收机制可以回收此处的元素
        self._data[self._head] = None
        self._head += 1
        return res

    def _resize(self, capacity: int):
        capacity = max(capacity, self.MIN_SIZE)

        new = [None for _ in range(capacity)]
        new[:len(self)] = list(self)
        # 这里必须用 tuple unpack, 因为 `len(self)` 的计算跟 `self._head` 有关
        self._head, self._tail = 0, len(self)
        self._data = new

    @property
    def _capacity(self) -> int:
        return len(self._data)


class LoopArrayV2:
    """循环数组.

    循环数组有以下关键点:

        1. 指针向右移动时需要 mod 操作来实现循环.
        2. 改变容量时注意需要将头尾指针重置.
        3. 当动态数组为空或满时头尾指针都将重合, 需要通过数组的大小来判断具体是哪种, 然后进行不同的处理.

    实际上 `_size` 这个变量就是用于解决上面的第三点问题. 如果头尾指针不重合, 那么动态数组的大小都是可以由
    `_head` 和 `_tail` 计算出来的, 但重合时只靠头尾指针就不够了. 当然这个问题还有很多的解决办法,
    只不过我认为记一个 `_size` 是最清晰的解决方式了.

    本数据结构只实现左进, 左出, 右进, 右出.
    """

    MIN_SIZE = 10

    def __init__(self):
        self._data = [None for _ in range(self.MIN_SIZE)]
        self._tail = 0
        self._head = 0
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator:
        # 如果按照 `self._head` 和 `self._tail` 定位动态数组
        # 的范围, 那么一定不要忘记当二者相等时可能动态数组是空的也可能是满的.
        for i in range(len(self)):
            yield self._data[self._move(self._head, i)]

    def append(self, value: Any):
        # 扩容
        if len(self) == self._capacity:
            self._resize(2 * self._capacity)

        self._data[self._tail] = value
        self._tail = self._move(self._tail, offset=1)
        self._size += 1

    def appendleft(self, value: Any):
        # 扩容
        if len(self) == self._capacity:
            self._resize(2 * self._capacity)

        self._head = self._move(self._head, offset=-1)
        self._data[self._head] = value
        self._size += 1

    @not_empty
    def pop(self) -> Any:
        self._tail = self._move(self._tail, offset=-1)
        res = self._data[self._tail]
        # 让垃圾回收机制可以回收此处的元素
        self._data[self._tail] = None
        self._size -= 1

        # 缩容
        if len(self) == self._capacity // 4:
            self._resize(self._capacity // 2)

        return res

    @not_empty
    def popleft(self) -> Any:
        res = self._data[self._head]
        # 让垃圾回收机制可以回收此处的元素
        self._data[self._head] = None
        self._head = self._move(self._head, offset=1)
        self._size -= 1

        # 缩容
        if len(self) == self._capacity // 4:
            self._resize(self._capacity // 2)

        return res

    def _move(self, index: int, offset: int) -> int:
        # 在 Python 中 -1 % 10 == 9
        return (index + offset) % self._capacity

    def _resize(self, capacity: int):
        if capacity < self.MIN_SIZE:
            return

        new = [None for _ in range(capacity)]
        new[:len(self)] = list(self)
        self._head = 0
        self._tail = len(self)
        self._data = new

    @property
    def _capacity(self) -> int:
        return len(self._data)


class LoopArrayV3:
    """循环数组.

    在 `LoopArrayV2` 的基础上通用化插入和删除功能.

    需要注意:

      1. 所有方法中传入的 `index` 都是动态数组索引 (相对索引), 不是底层静态数组的索引.
         公式: real_index = (head + relative_index) % capacity
      2. 插入和删除元素前需要选择移动哪个指针, 选择指针的方式如下:
         ```
         [0, 1, 2], 3 // 2 == 1, 当索引 >= 1 时, 移动尾指针, 其余移动首指针.
         [0, 1, 2, 3], 4 // 2 == 2, 当索引 >= 2 时, 移动尾指针, 其余移动首指针.
         ```
      3. 由于第二条注意事项, 当数组为空时插入元素, 无论调用 `popleft` 还是 `pop` 都是移动尾指针.
         当数组只有一个元素时删除元素, 无论调用 `append` 还是 `appendleft` 都是移动尾指针.
         举例说明下这个注意事项的意义, 假设先 `append` 2 个元素, 再 `popleft` 2 个元素,
         可能第一反应是尾指针向右移动两位, 首指针也向右移动两位. 但实际情况是尾指针先向右移动两位,
         首指针向右移动一位, 然后尾指针向左移动一位.
    """

    MIN_SIZE = 10

    def __init__(self):
        self._data = [None for _ in range(self.MIN_SIZE)]
        self._tail = 0
        self._head = 0
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator:
        # 如果按照 `self._head` 和 `self._tail` 定位动态数组
        # 的范围, 那么一定不要忘记当二者相等时可能动态数组是空的也可能是满的.
        for i in range(len(self)):
            yield self._data[self._move(self._head, i)]

    @check_index()
    def __getitem__(self, index: int) -> Any:
        return self._data[self._move(self._head, offset=index)]

    @check_index()
    def __setitem__(self, index: int, value: Any):
        self._data[self._move(self._head, offset=index)] = value

    @check_index(offset=1)
    def insert(self, index: int, value: Any):
        # 扩容
        if len(self) == self._capacity:
            self._resize(2 * self._capacity)

        if index >= len(self) // 2:
            # 尾指针右移, [index, len) -> [index + 1, len + 1)
            for i in range(len(self), index, -1):
                real_i = self._move(self._head, offset=i)
                self._data[real_i] = self._data[self._move(real_i, offset=-1)]
            self._tail = self._move(self._tail, offset=1)
        else:
            # 首指针左移, [0, index + 1) -> [-1, index)
            for i in range(-1, index):
                real_i = self._move(self._head, offset=i)
                self._data[real_i] = self._data[self._move(real_i, offset=1)]
            self._head = self._move(self._head, offset=-1)

        self._data[self._move(self._head, offset=index)] = value
        self._size += 1

    def append(self, value: Any):
        self.insert(len(self), value)

    def appendleft(self, value: Any):
        self.insert(0, value)

    @check_index()
    def remove(self, index: int) -> Any:
        if len(self) == 0:
            raise IndexError

        res = self._data[self._move(self._head, offset=index)]

        if index >= len(self) // 2:
            # 尾指针左移 [index + 1, len) -> [index, len - 1)
            for i in range(index, len(self) - 1):
                real_i = self._move(self._head, offset=i)
                self._data[real_i] = self._data[self._move(real_i, offset=1)]
            self._tail = self._move(self._tail, offset=-1)
            # 让垃圾回收机制可以回收此处的元素
            self._data[self._move(self._head, offset=len(self) - 1)] = None
        else:
            # 首指针右移 [0, index) -> [1, index + 1)
            for i in range(index, 0, -1):
                real_i = self._move(self._head, offset=i)
                self._data[real_i] = self._data[self._move(real_i, offset=-1)]
            # 让垃圾回收机制可以回收此处的元素
            self._data[self._move(self._head, offset=0)] = None
            self._head = self._move(self._head, offset=1)

        self._size -= 1

        # 缩容
        if len(self) == self._capacity // 4:
            self._resize(self._capacity // 2)

        return res

    def pop(self) -> Any:
        return self.remove(len(self) - 1)

    def popleft(self) -> Any:
        return self.remove(0)

    def _move(self, index: int, offset: int) -> int:
        return (index + offset) % self._capacity

    def _resize(self, capacity: int):
        if capacity < self.MIN_SIZE:
            return

        new = [None for _ in range(capacity)]
        new[:len(self)] = list(self)
        self._head = 0
        self._tail = len(self)
        self._data = new

    @property
    def _capacity(self) -> int:
        return len(self._data)
