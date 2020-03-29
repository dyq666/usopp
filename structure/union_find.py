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

    在本数据结构中, 并是 O(H), 查是 O(H) (H 是索引的高度). H 和 N 之间
    的关系比较复杂, 最终结论是: O(H) == O(log*N), O(log*N) 比 O(logN) 更快, 接近 O(1).
    https://en.wikipedia.org/wiki/Iterated_logarithm

    `self._parent` 的索引和值各代表什么 ?

    答: 索引代表每个实例的编号, 具体实例和编号的映射需要在并查集外部维护.
       值代表元素父亲的索引. 当索引和值相同时, 元素为根节点. 如果两个
       元素的根节点相同, 那么两个元素在一个集合中.

    `self._rank` 的索引和值各代表什么 ?

    答: 索引和 `_parent` 中的索引意义相同. 如果不使用路径压缩优化, 那么
       值代表以当前索引为根的树层数. 使用路径压缩优化后, 值就代表一个相对
       评分, 原因是路径压缩过程中, 无法简单计算压缩之后树的层数, 因而无法
       更新层数, 但这并不影响合并时比较两个树. 这也就是为什么这个变量叫做
       rank 而不是 depth 的原因.
    """

    def __init__(self, parent: List[int], rank: List[int]):
        self._parent = parent
        self._rank = rank

    def __len__(self) -> int:
        return len(self._parent)

    def is_connected(self, idx1: int, idx2: int) -> bool:
        """两个元素是否在一个集合中 ?"""
        return self._root(idx1) == self._root(idx2)

    def union(self, idx1: int, idx2: int):
        """合并两个元素所在的集合.

        合并时将层数少的树合并到层数多的树中, 这样树的高度比反过来更低.
        """
        root1, root2 = self._root(idx1), self._root(idx2)
        rank1, rank2 = self._rank[root1], self._rank[root2]
        if rank1 < rank2:
            self._parent[root1] = root2
            self._rank[root2] = max(rank2, rank1 + 1)
        else:
            self._parent[root2] = root1
            self._rank[root1] = max(rank1, rank2 + 1)

    @check_index()
    def _root(self, index: int) -> int:
        """查找元素的根节点."""
        # 当索引和值相同时, 元素为根节点.
        while index != self._parent[index]:
            # 路径压缩, 减小树的层数. 让节点的父索引指向节点的爷爷索引, 由于根节点也有父索引 (是它自己),
            # 所以非根节点以外的所有节点都有爷爷索引, 因此不会触发 `IndexError`.
            self._parent[index] = self._parent[self._parent[index]]
            index = self._parent[index]
        return index

    @classmethod
    def generate(cls, size: int) -> 'UnionFindV2':
        # 初始时, 每个元素都是根节点 (值和索引相同), 每棵树的层数都为 1.
        return UnionFindV2(list(range(size)), [1 for _ in range(size)])
