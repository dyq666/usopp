__all__ = (
    'UnionFindV1',
)

from typing import List


class UnionFindV1:
    """并查集 V1.

    在本数据结构中, 并是 O(N), 查是 O(1).

    `self._ids` 的索引和值各代表什么 ?

    答: 索引代表每个实例的编号, 具体实例和编号的映射需要在并查集外部维护.
       值代表元素所在集合的 id, 如果两个元素的集合 id 相同, 那么两个元素在一个集合中.
    """

    def __init__(self, ids: List[int]):
        self._ids = ids

    def __len__(self) -> int:
        return len(self._ids)

    def is_connected(self, p: int, q: int) -> bool:
        if not (0 <= p < len(self) and 0 <= q < len(self)):
            raise IndexError
        return self._ids[p] == self._ids[q]

    def union(self, p: int, q: int):
        if not (0 <= p < len(self) and 0 <= q < len(self)):
            raise IndexError
        p_id, q_id = self._ids[p], self._ids[q]
        # 把和 p 在一个集合的所有元素, 移动到 q 所在的集合中.
        for i in range(len(self)):
            if self._ids[i] == p_id:
                self._ids[i] = q_id

    @classmethod
    def generate(cls, size: int) -> 'UnionFindV1':
        return UnionFindV1([i for i in range(size)])
