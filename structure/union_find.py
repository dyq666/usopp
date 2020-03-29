__all__ = (
    'UnionFindV1', 'UnionFindV2',
)

from typing import List

from .util import check_index


class UnionFindV1:
    """并查集 V1.

    在本数据结构中, 并是 O(N), 查是 O(1).

    `self._ids` 的索引和值各代表什么 ?

    答: 索引代表每个实例的编号, 具体实例和编号的映射需要在并查集外部维护.
       值代表元素所在集合的 id, 如果两个元素的集合 id 相同, 那么两个元素在一个集合中.
    """

    def __init__(self, ids: List[int]):
        self._set_id = ids

    def __len__(self) -> int:
        return len(self._set_id)

    def is_connected(self, idx1: int, idx2: int) -> bool:
        """两个元素是否在一个集合中 ?"""
        return self._set(idx1) == self._set(idx2)

    def union(self, idx1: int, idx2: int):
        """合并两个元素所在的集合."""
        set1, set2 = self._set(idx1), self._set(idx2)

        if set1 == set2:
            return

        # 把和 idx1 在一个集合的所有元素, 移动到 idx2 所在的集合中.
        for i in range(len(self)):
            if self._set(i) == set1:
                self._set_id[i] = set2

    @check_index()
    def _set(self, index: int) -> int:
        """查找元素所在的集合 id."""
        return self._set_id[index]

    @classmethod
    def generate(cls, size: int) -> 'UnionFindV1':
        # 初始时, 每个元素都独自在一个集合中.
        return UnionFindV1(list(range(size)))


class UnionFindV2:
    """并查集 V2.

    在本数据结构中, 并是 O(H), 查是 O(H), H 是索引的高度, H << N.

    `self._parent` 的索引和值各代表什么 ?

    答: 索引代表每个实例的编号, 具体实例和编号的映射需要在并查集外部维护.
       值代表元素父亲的索引. 当索引和值相同时, 元素为根节点. 如果两个
       元素的根节点相同, 那么两个元素在一个集合中.
    """

    def __init__(self, parent: List[int]):
        self._parent = parent

    def __len__(self) -> int:
        return len(self._parent)

    def is_connected(self, idx1: int, idx2: int) -> bool:
        """两个元素是否在一个集合中 ?"""
        return self._root(idx1) == self._root(idx2)

    def union(self, idx1: int, idx2: int):
        """合并两个元素所在的集合.

        合并时必须将一个根节点指向另一个根节点, 这样可以最大程度的减小树的高度.
        虽然让 idx1 的根节点指向 idx2, 也可以完成合并操作, 但会增加树的高度.
        """
        self._parent[self._root(idx1)] = self._root(idx2)

    @check_index()
    def _root(self, index: int) -> int:
        """查找元素的根节点."""
        # 当索引和值相同时, 元素为根节点.
        while index != self._parent[index]:
            index = self._parent[index]
        return index

    @classmethod
    def generate(cls, size: int) -> 'UnionFindV2':
        # 初始时, 每个元素都是根节点.
        return UnionFindV2(list(range(size)))
