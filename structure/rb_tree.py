__all__ = (
    'Tree23',
)

from typing import Generator, Iterator, List, Optional

from .typing_ import Comparable


class Node23:

    def __init__(self,
                 keys: Optional[List[Comparable]] = None,
                 children: Optional[List['Node23']] = None):
        self.keys = [] if keys is None else keys
        self.children = [] if children is None else children

    def preorder(self) -> Generator['Node23', None, None]:
        """前序遍历."""
        nodes = [self]
        while nodes:
            n = nodes.pop()
            yield n
            nodes.extend(reversed(self.children))


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
            self._add(self._root, key)

    def _add(self, root: Node23, key: Comparable):
        pass
