__all__ = (
    'Tree23',
)

import bisect
from typing import Generator, Iterable, Iterator, List, Optional

from .typing_ import Comparable


class Node23:

    def __init__(self,
                 keys: Optional[List[Comparable]] = None,
                 children: Optional[List['Node23']] = None):
        self.keys = [] if keys is None else keys
        self.children = [] if children is None else children

    @property
    def isleaf(self) -> bool:
        return not self.children

    def add(self, key: Comparable):
        bisect.insort(self.keys, key)

    def preorder(self) -> Generator['Node23', None, None]:
        """前序遍历."""
        nodes = [self]
        while nodes:
            n = nodes.pop()
            yield n
            nodes.extend(reversed(n.children))


class Tree23:
    """二三树.

    为什么叫二三树 ? 因为每个节点中可以有 1-2 个值, 相应的有 2-3 个孩子节点,
    len(孩子节点) = len(节点值) + 1. 另外按照二分搜索树的方式命名, 可能叫做
    二三分搜索平衡树.
    """

    def __init__(self):
        self._size = 0
        self._root: Optional[Node23] = None

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[List[Comparable]]:
        return (n.keys for n in self._root.preorder())

    def add(self, key: Comparable):
        """添加 `key`.

        二三树是一棵绝对平衡的树, 永远不会向空的位置添加节点 (除非是根节点),
        例如按顺序插入 42 37 12 18 6 11 5:
        ```
        (根节点, 只能在空的位置添加节点)
        42

        (由于不能向空添加节点, 因此 37 不能插入到 42 的孩子节点, 只能和 42 放在一个节点中)
        37,42

        (由于不能向空添加节点, 因此 12 不能插入到 37,42 的孩子节点,
         只能先和 37,42 放在一个节点中, 然后在分裂)
        12,37,42           37
                   ->    12 42

              37
        12,18   42

                37             37          12,37
        6,12,18   42    ->   12  42   ->  6 18 42
                            6  18

            12,37
        6,11 18 42

              12,37            12,37         6,12,37            12
        5,6,11 18 42   ->    6  18 42  ->  5 11 18 42   ->    6    37
                           5 11                             5 11 18 42
        ```
        """
        if self._root is None:
            self._root = Node23([key])
            self._size += 1
        else:
            self._root = self._add(self._root, key)

    @classmethod
    def from_iterable(cls, keys: Iterable[Comparable]) -> 'Tree23':
        tree = cls()
        for k in keys:
            tree.add(k)
        return tree

    def _add(self, root: Node23, key: Comparable) -> Node23:
        if root.isleaf:
            # TODO 如果将来做成 k/v 的模式, 这里要更新
            # TODO 这个查询操作是 O(N) 的, 可能不太好.
            if key in root.keys:
                return root

            root.add(key)
            self._size += 1
            # 1,2    ->   1,2
            if len(root.keys) == 2:
                return root
            #               2
            # 1,2,3  ->   1   3
            if len(root.keys) == 3:
                return Node23([root.keys[1]], children=[
                    Node23([root.keys[0]]),
                    Node23([root.keys[2]]),
                ])

    def _split(self, root: Node23):
        """

        应该一个节点中有三个 key 只有下面两种情况.
        # TODO 需要确认这个是否只有这两种情况.

        ```
          2,4,6    ->     4
                        2   6

                          4
          2,4,6    ->   2   6
         1 3 5 7       1 3 5 7
        ```
        """
        children = root.children
        keys = root.keys
        if children:
            pass
        else:
            pass
