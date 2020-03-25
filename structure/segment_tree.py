__all__ = (
    'SegmentTree',
)

from typing import Any, Iterable

from .tree import BTUtil
from .util import check_index


class SegmentTree:

    def __init__(self, array: list, tree: list, key: callable):
        self._a = array
        self._t = tree
        self.key = key

    def __len__(self) -> int:
        return len(self._a)

    @check_index()
    def __setitem__(self, index: int, value: Any):
        self._a[index] = value
        self._update(0, len(self) - 1, index, value, root=0)

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
        """在以 `root` 为根的线段树中查询 [query_l...query_r] 区间,
        根代表的区间为 [l...r].
        """
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

    def _update(self, l: int, r: int, target_idx: int, value: Any, root: int):
        """在以 `root` 为根的线段树中, 更新包含 `target_idx` 的区间, 根代表的区间为 [l...r]."""
        if l == r == target_idx:
            self._t[root] = self._a[l]
            return

        # 区间分为 [l...mid], [mid+1...r]
        mid = (l + r) // 2

        # target_idx 只可能在左区间或右区间
        if target_idx <= mid:
            self._update(l, mid, target_idx, value, root=BTUtil.left_idx(root))
        else:
            self._update(l, mid, target_idx, value, root=BTUtil.right_idx(root))
        self._t[root] = self._merge(root)
