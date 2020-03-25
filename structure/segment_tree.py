__all__ = (
    'SegmentTree', 'SegmentTreeWithNode',
)

import itertools
from typing import Any, Iterable, Optional

from .tree import BTNode, BTUtil
from .util import check_index


class SegmentTree:

    def __init__(self, array: list, tree: list, key: callable):
        self._a = array
        self._t = tree
        self.key = key

    def __len__(self) -> int:
        return len(self._a)

    def __iter__(self) -> Iterable:
        return itertools.takewhile(lambda o: o is not None, self._t)

    @check_index()
    def __setitem__(self, index: int, value: Any):
        self._a[index] = value
        self._update(0, len(self) - 1, target_idx=index, root=0)

    def query(self, l: int, r: int) -> Any:
        if not (0 <= l < len(self) and 0 <= r < len(self) and l <= r):
            raise IndexError
        return self._query(0, len(self) - 1, root=0, query_l=l, query_r=r)

    @classmethod
    def from_iterable(cls, iterable: Iterable, key: callable
                      ) -> 'SegmentTree':
        """根据 `iterable` 创建线段树, `key` 是融合函数.

        TODO 在这解释为什么 `tree` 是 `array` 的四倍.
        """
        array = list(iterable)
        tree = [None for _ in range(len(array) * 4)]
        segement = cls(array, tree, key=key)
        segement._build(0, len(segement) - 1, root=0)
        return segement

    def _build(self, l: int, r: int, root: int):
        """以 `root` 为根构建线段树, 根代表的区间为 [l...r]."""
        # 无效区间
        if l > r:
            return
        # 区间无法再分割了
        if l == r:
            self._t[root] = self._a[l]
            return

        # 区间分为 [l...mid], [mid+1...r]
        mid = (l + r) // 2

        # 后序遍历, 左节点代表左区间, 右节点代表右区间
        self._build(l, mid, root=BTUtil.left_idx(root))
        self._build(mid + 1, r, root=BTUtil.right_idx(root))
        self._t[root] = self._merge(root)

    def _merge(self, root: int) -> Any:
        """融合孩子节点得到父节点的值."""
        return self.key(self._t[BTUtil.left_idx(root)],
                        self._t[BTUtil.right_idx(root)])

    def _query(self, l: int, r: int, root: int, query_l: int, query_r: int) -> Any:
        """在以 `root` 为根的线段树中查询区间 [query_l...query_r], 根代表的区间为 [l...r]."""
        if l == query_l and r == query_r:
            return self._t[root]

        # 区间分为 [l...mid], [mid+1...r]
        mid = (l + r) // 2

        # 如果查询区间是左或右区间的子集, 那么直接去左或右查
        if query_r <= mid:
            return self._query(l, mid, root=BTUtil.left_idx(root),
                               query_l=query_l, query_r=query_r)
        if query_l >= mid + 1:
            return self._query(mid + 1, r, root=BTUtil.right_idx(root),
                               query_l=query_l, query_r=query_r)
        # 查询区间横跨两个区间, 那么把查询区间分为 [query_l...mid], [mid+1...query_r]
        vl = self._query(l, mid, root=BTUtil.left_idx(root),
                         query_l=query_l, query_r=mid)
        vr = self._query(mid + 1, r, root=BTUtil.right_idx(root),
                         query_l=mid + 1, query_r=query_r)
        return self.key(vl, vr)

    def _update(self, l: int, r: int, target_idx: int, root: int):
        """在以 `root` 为根的线段树中, 更新包含 `target_idx` 的区间, 根代表的区间为 [l...r]."""
        if l == r == target_idx:
            self._t[root] = self._a[l]
            return

        # 区间分为 [l...mid], [mid+1...r]
        mid = (l + r) // 2

        # `target_idx` 只可能在左区间或右区间
        if target_idx <= mid:
            self._update(l, mid, target_idx, root=BTUtil.left_idx(root))
        else:
            self._update(l, mid, target_idx, root=BTUtil.right_idx(root))
        self._t[root] = self._merge(root)


class SegmentTreeWithNode:

    def __init__(self, array: list, key: callable):
        self._a = array
        self.key = key
        self.root: Optional[BTNode] = None

    def __len__(self) -> int:
        return len(self._a)

    def __iter__(self) -> Iterable:
        return (n.val for level in BTUtil.levelorder(self.root) for n in level)

    @check_index()
    def __setitem__(self, index: int, value: Any):
        self._a[index] = value
        self._update(0, len(self) - 1, target_idx=index, root=self.root)

    def query(self, l: int, r: int) -> Any:
        if not (0 <= l < len(self) and 0 <= r < len(self) and l <= r):
            raise IndexError
        return self._query(0, len(self) - 1, root=self.root, query_l=l, query_r=r)

    @classmethod
    def from_iterable(cls, iterable: Iterable, key: callable
                      ) -> 'SegmentTreeWithNode':
        """根据 `iterable` 创建线段树, `key` 是融合函数."""
        array = list(iterable)
        segement = cls(array, key=key)
        segement.root = segement._build(0, len(segement) - 1)
        return segement

    def _build(self, l: int, r: int) -> Optional[BTNode]:
        """以 `node` 为根构建线段树, 根代表的区间为 [l...r]."""
        # 无效区间
        if l > r:
            return
        # 区间无法再分割了
        if l == r:
            return BTNode(self._a[l])

        # 区间分为 [l...mid], [mid+1...r]
        mid = (l + r) // 2

        # 后序遍历, 左节点代表左区间, 右节点代表右区间
        node_l = self._build(l, mid)
        node_r = self._build(mid + 1, r)
        return BTNode(self.key(node_l.val, node_r.val), node_l, node_r)

    def _query(self, l, r, root: BTNode, query_l, query_r) -> Any:
        """在以 `root` 为根的线段树中查询 [query_l...query_r], 根代表的区间为 [l...r]."""
        if l == query_l and r == query_r:
            return root.val

        # 区间分为 [l...mid], [mid+1...r]
        mid = (l + r) // 2

        # 如果查询区间是左或右区间的子集, 那么直接去左或右查
        if query_r <= mid:
            return self._query(l, mid, root=root.left,
                               query_l=query_l, query_r=query_r)
        elif query_l >= mid + 1:
            return self._query(mid + 1, r, root=root.right,
                               query_l=query_l, query_r=query_r)
        # 查询区间横跨两个区间, 那么把查询区间分为 [query_l...mid], [mid+1...query_r]
        vl = self._query(l, mid, root=root.left, query_l=query_l, query_r=mid)
        vr = self._query(mid + 1, r, root=root.right, query_l=mid + 1, query_r=query_r)
        return self.key(vl, vr)

    def _update(self, l: int, r: int, target_idx: int, root: BTNode):
        """在以 `root` 为根的线段树中, 更新包含 `target_idx` 的区间, 根代表的区间为 [l...r]."""
        if l == r == target_idx:
            root.val = self._a[l]
            return

        # 区间分为 [l...mid], [mid+1...r]
        mid = (l + r) // 2

        # `target_idx` 只可能在左区间或右区间
        if target_idx <= mid:
            self._update(l, mid, target_idx=target_idx, root=root.left)
        else:
            self._update(mid + 1, r, target_idx=target_idx, root=root.right)
        root.val = self.key(root.left.val, root.right.val)
