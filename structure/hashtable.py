__all__ = (
    'HashTable',
)

from typing import Any, List, Iterator, Tuple

from .typing_ import Hashable
from .util import EquablePair


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

    为什么要模一个质数 ? 首先我们希望哈希值尽可能分布均匀, 越均匀哈希冲突越少.
    如果数据均匀分布, 那么模任意一个数得到的哈希值都是均匀分布的. 如果数据分布
    不均匀, 那么通常模一个质数可以使哈希值分布更均匀.

    如何将数据转换成整数 ?
      - 浮点数. 浮点数在底层是 32 位 / 64 位的大小, 我们直接将这些位看成 int 即可.
      - 字符串. 字符串不能像浮点数一样, 直接把底层的大小看成 int, 因为字符串是动态数据,
               底层大小不确定, 而且很可能超出 int 可承受的范围, 因而需要使用其他转换
               方式. 假设字符串中只有 26 个小写字母, 那么可以将字符串看成 26 进制:
                 ```
                 对于一个 10 进制的数来说, 134 = 1 * 10 ^ 2 + 3 * 10 ^ 1 + 4 * 10 ^ 0.
                 因而, 对于一个 26 进制的数来说, ice = 9 * 26 ^ 2 + 3 * 26 ^ 1 + 5 * 26 ^ 0.
                 ```
               那么, 如果字符串中有 B 种字符, 那么可以将字符串看成 B 进制, 此时 ice
               就不是在 26 进制下的一个整数了, 而是 B 进制下的一个整数:
                 ```
                 ice = 9 * B ^ 2 + 3 * B ^ 1 + 5 * 26 ^ 0.
                 因为幂运算比较慢, 因此可以将公式变为: ice = (9 * B + 3) * B + 5.
                 ```
               另外 B 的选择不一定非得和实际种类相同, 可以根据实际情况调整.
      - 其他类型. 例如有个 Student 类型, 属性有学号 (int), 评分 (float), 姓名 (float).
                由于学号不可能重复, 因而我们可以直接用学号作为此类的哈希值. 另外更通用的做法
                是, 将所有属性组合起来转成一个哈希值, 我们先将所有类型按照上述规则转成 int.
                然后按照字符串中的做法选择一个进制 B, 最终哈希值就等于:
                  ```
                  hash = self.id * B ^ 2 + hash(self.float) * B ^ 1 + hash(self.name) * B ^ 0.
                  ```
                总结, 尽可能将自定义类型转成均匀分布的 int.
    """

    CAPACITYS = [53, 97, 193, 389, 769]  # 质数来源: https://planetmath.org/goodhashtableprimes
    UPPER = 10
    LOWER = 2

    def __init__(self):
        self._size = 0
        self._capacity_idx = 0
        self._groups: List[List[EquablePair]] = [[] for _ in range(self._capacity)]

    def __iter__(self) -> Iterator[Tuple[Hashable, Any]]:
        for group in self._groups:
            for pair in group:
                yield pair.key, pair.value

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: Hashable) -> bool:
        return EquablePair(key, None) in self._group(key)

    def add(self, key: Hashable, value: Any):
        group = self._group(key)

        try:
            idx = group.index(EquablePair(key, None))
        except ValueError:
            # 不存在, 新增.
            group.append(EquablePair(key, value))
            self._size += 1
            if len(self) > self._capacity * self.UPPER:
                self._resize(is_increase=True)
        else:
            # 已经存在, 更新旧值.
            group[idx] = EquablePair(key, value)

    def get(self, key: Hashable) -> Any:
        """如果 `key` 不存在, 会抛出 KeyError."""
        group = self._group(key)
        try:
            idx = group.index(EquablePair(key, None))
        except ValueError:
            raise KeyError
        else:
            return group[idx].value

    def remove(self, key: Hashable):
        """如果 `key` 不存在, 会抛出 KeyError."""
        try:
            self._group(key).remove(EquablePair(key, None))
        except ValueError:
            raise KeyError
        else:
            self._size -= 1
            if len(self) < self._capacity * self.LOWER:
                self._resize(is_increase=False)

    @property
    def _capacity(self) -> int:
        return self.CAPACITYS[self._capacity_idx]

    def _hash(self, key: Hashable) -> int:
        """计算哈希值."""
        return abs(hash(key)) % self._capacity

    def _group(self, key: Hashable) -> list:
        return self._groups[self._hash(key)]

    def _resize(self, is_increase: bool):
        """修改容量.

        `is_increase`: True 代表扩容, False 代表缩容.
        """
        new_capacity_idx = self._capacity_idx + (1 if is_increase else -1)
        if not (0 <= new_capacity_idx < len(self.CAPACITYS)):
            return

        # 注意这里必须先更新容量, 下面计算哈希值 `self._hash` 和
        # 计算容量 `self._capacity` 都会依赖此属性.
        self._capacity_idx = new_capacity_idx
        new_groups = [[] for _ in range(self._capacity)]
        for k, v in self:
            group = new_groups[self._hash(k)]
            group.append(EquablePair(k, v))
        self._groups = new_groups
