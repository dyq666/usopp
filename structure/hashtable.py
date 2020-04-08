__all__ = (
    'HashTable',
)

from typing import Any, List, Iterator, Optional, Tuple

from .util import HashPair


class StudentV1:

    def __init__(self, grade: int, class_: int, name: str):
        self.grade = grade
        self.class_ = class_
        self.name = name


class StudentV2:

    def __init__(self, grade: int, class_: int, name: str):
        self.grade = grade
        self.class_ = class_
        self.name = name

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.grade == other.grade
            and self.class_ == other.class_
            and self.name == other.name
        )

    def __hash__(self) -> int:
        # hash = self.grade * B^2 + self.class_ * B^1 + hash(self.name) * B^0
        # hash = (self.grade * B + self.class_) * B + hash(self.name)
        val = 0
        for attr in (self.grade, self.class_, hash(self.name)):
            # B 实际上可以是任意值, 这里选用 B = 26.
            val = val * 26 + attr
        return val


class HashTable:
    """哈希表.

    使用链地址法 (separate chaining) 解决哈希冲突, 其中的一些细节如下:

      - 本类使用 Python 底层的 list 代替链表.
      - 预置一些质数 `cls.CAPACITYS` 用于容量的扩展或缩小.
      - 当元素数量大于容量的 `cls.UPPER` 倍时, 进行扩容 (也可以认为每组最多有 `cls.UPPER` 个元素).
      - 当元素数量小于容量的 `cls.LOWER` 倍时, 进行缩容 (也可以认为每组最少有 `cls.LOWER` 个元素).

    个人对链地址法的理解: 链地址法可以看作对数据分组, 每个数据只能在组内
    进行增删改查. 数据通过哈希函数找到自己的组 id, 组和组 id 的关系就是
    底层数组和索引的关系, 因为这个找组的操作是许多函数的第一步, 所以封装了
    一个函数 `self._group`. 另外, 改变容量 (`self._resize`) 意味
    着对所有数据重新分组.

    时间复杂度分析: 每一组只有 `cls.LOWER` ~ `cls.UPPER` 个元素, 所以组内操作的
    时间复杂度只有 O(LOWER) ~ O(UPPER), 即 O(1). 而 resize 中的时间可以均摊到
    每次操作中, 也是 O(1) 的.
    """

    CAPACITYS = [53, 97, 193, 389, 769]  # 质数来源: https://planetmath.org/goodhashtableprimes
    UPPER = 10
    LOWER = 2

    def __init__(self):
        self._size = 0
        self._capacity_idx = 0
        self._groups: List[List[HashPair]] = [[] for _ in range(self.CAPACITYS[self._capacity_idx])]

    def __iter__(self) -> Iterator[Tuple[Any, Any]]:
        for group in self._groups:
            for pair in group:
                yield pair.key, pair.value

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: Any) -> bool:
        return HashPair(key, None) in self._group(key)

    def add(self, key: Any, value: Any = 0):
        group = self._group(key)

        try:
            idx = group.index(HashPair(key, None))
        except ValueError:
            # 不存在, 新增.
            group.append(HashPair(key, value))
            self._size += 1
            if len(self) > self._capacity * self.UPPER:
                self._resize(is_increase=True)
        else:
            # 已经存在, 更新旧值.
            group[idx] = HashPair(key, value)

    def get(self, key: Any) -> Any:
        """如果不存在 `key`, 会抛出 KeyError."""
        group = self._group(key)
        try:
            idx = group.index(HashPair(key, None))
        except ValueError:
            raise KeyError
        else:
            return group[idx].value

    def remove(self, key: Any):
        """如果不存在 `key`, 会抛出 KeyError."""
        try:
            self._group(key).remove(HashPair(key, None))
        except ValueError:
            raise KeyError
        else:
            self._size -= 1
            if len(self) < self._capacity * self.LOWER:
                self._resize(is_increase=False)

    @property
    def _capacity(self) -> int:
        return self.CAPACITYS[self._capacity_idx]

    def _hash(self, key: Any, capacity: Optional[int] = None) -> int:
        """计算哈希值."""
        capacity = self._capacity if capacity is None else capacity
        return abs(hash(key)) % capacity

    def _group(self, key: Any) -> list:
        return self._groups[self._hash(key)]

    def _resize(self, is_increase: bool):
        """修改容量.

        `is_increase`: True 代表扩容, False 代表缩容.
        """
        new_capacity_idx = self._capacity_idx + (1 if is_increase else -1)
        if not (0 <= new_capacity_idx < len(self.CAPACITYS)):
            return

        new_capacity = self.CAPACITYS[new_capacity_idx]
        new_groups = [[] for _ in range(new_capacity)]
        for k, v in self:
            group = new_groups[self._hash(k, new_capacity)]
            group.append(HashPair(k, v))

        self._groups = new_groups
        self._capacity_idx = new_capacity_idx
