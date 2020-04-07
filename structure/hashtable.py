__all__ = (
    'HashTable',
)

from typing import Any, Iterator, Optional, Tuple

from .tree import BSTDict


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
    """哈希表 (链地址法).

    哈希表中每一个节点都是一个二分搜索树.
    """

    DICT_CLS = BSTDict
    CAPACITYS = [53, 97, 193, 389, 769]  # 一些质数
    UPPER = 10  # 当 size 大于 capacity 的 10 倍时, 扩容
    LOWER = 2  # 当 size 小于 capacity 的 2 倍时, 缩容

    def __init__(self):
        self._size = 0
        self._capacity_idx = 0
        self._dicts = [self.DICT_CLS() for _ in range(self.CAPACITYS[self._capacity_idx])]

    def __iter__(self) -> Iterator[Tuple[Any, Any]]:
        for dict_ in self._dicts:
            yield from dict_

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: Any) -> bool:
        return key in self._dicts[self._hash(key)]

    def __setitem__(self, key: Any, value: Any):
        dict_ = self._dicts[self._hash(key)]

        if key not in dict_:
            dict_[key] = value
            self._size += 1
            if len(self) > self._capacity * self.UPPER:
                self._resize(True)
        # 如果已经存在的话, 更新值
        else:
            dict_[key] = value

    def __getitem__(self, key: Any) -> Any:
        return self._dicts[self._hash(key)][key]

    def __delitem__(self, key: Any):
        del self._dicts[self._hash(key)][key]
        self._size -= 1
        if len(self) < self._capacity * self.LOWER:
            self._resize(False)

    @property
    def _capacity(self) -> int:
        return self.CAPACITYS[self._capacity_idx]

    def _hash(self, key: Any, capacity: Optional[int] = None) -> int:
        capacity = self._capacity if capacity is None else capacity
        return abs(hash(key)) % capacity

    def _resize(self, is_increase: bool):
        new_capacity_idx = self._capacity_idx + (1 if is_increase else -1)
        if new_capacity_idx < 0 or new_capacity_idx >= len(self.CAPACITYS):
            return

        self._capacity_idx = new_capacity_idx
        new_capacity = self.CAPACITYS[self._capacity_idx]
        new_dicts = [self.DICT_CLS() for _ in range(new_capacity)]

        for k, v in self:
            dict_ = new_dicts[self._hash(k, new_capacity)]
            dict_[k] = v
        self._dicts = new_dicts
