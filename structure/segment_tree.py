__all__ = (
    'SegmentTree', 'SegmentTreeWithNode',
)

import itertools
from typing import Any, Iterable, Iterator, Optional

from .tree import BTNode, BTUtil
from .util import check_index


class SegmentTree:
    """线段树 (数组存储).

    在线段树中, 节点代表的区间和节点对应的数组索引是一个节点必需的基本信息,
    因此在几乎所有方法中都有 `l r root` 三个参数.

    可用 LeetCode 307 测试. 另外需要注意线段树应该用于动态更新的场景,
    对于 LeetCode 303 来说, 数组是静态的不需要使用线段树.
    """

    def __init__(self, array: list, tree: list, key: callable):
        self._a = array
        self._t = tree
        self.key = key

    def __len__(self) -> int:
        return len(self._a)

    def __iter__(self) -> Iterator:
        return itertools.takewhile(lambda o: o is not None, self._t)

    @check_index()
    def __setitem__(self, index: int, value: Any):
        self._a[index] = value
        self._update(0, len(self) - 1, root=0, target_idx=index)

    def query(self, l: int, r: int) -> Any:
        if not (0 <= l < len(self) and 0 <= r < len(self) and l <= r):
            raise IndexError
        return self._query(0, len(self) - 1, root=0, query_l=l, query_r=r)

    @classmethod
    def from_iterable(cls, iterable: Iterable, key: callable
                      ) -> 'SegmentTree':
        """根据 `iterable` 创建线段树, `key` 是融合函数.

        N 个元素的数组为什么要用 4N 大小的树存储 ?

        答: 在层数相等的情况下, 满二叉树总会比完全二叉树多几个节点, 因此只要满二叉树
        能解决问题, 那么其他完全二叉树也就必能解决问题了. 在满二叉树中, 假设最后一层
        大小是 A, 那么树的大小 = 2A + 2A - 1 ~= 4A. 因此问题变为找到满二叉树最后
        一层的元素个数. 在最坏情况下, N 个元素都在满二叉树最后一层, 此时如果有某个大小
        能保证足够构建线段树, 那么其他情况, 就一定能够构建线段树. 而满二叉树每层节点的
        个数是 2 的指数, 那么需要计算能容纳 N 个元素的最小的 2 的指数. 而整课树的大小
        只要大于等于这个最小值 * 2 即可. 例如当 N = 9 时, 整棵树大小 >= 16 * 2 即可,
        当 N = 8 时, >= 8 * 2 即可. 然而在寻找 2 的指数的过程中涉及了 log 运算,
        log 运算比较耗时, 因而希望有别的方法代替它. 当 N = 9 时, 最小符合值是 32,
        而 32 = 4 * 8 < 4 * 9, 当 N = 8 时, 最小符合值是 16, 而 16 = 2 * 8 < 4 * 8,
        因此 4N 的大小一定满足此问题. 这是一种用空间换时间的方式 !
        """
        array = list(iterable)
        tree = [None for _ in range(len(array) * 4)]
        segement = cls(array, tree, key=key)
        segement._build(0, len(segement) - 1, root=0)
        return segement

    def _build(self, l: int, r: int, root: int):
        """以 `root` 为根, 构建表示区间 [l...r] 的线段树."""
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
        self._t[root] = self.key(self._t[BTUtil.left_idx(root)],
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
        # 查询左区间去左区间查, 查询右区间去右查.
        vl = self._query(l, mid, root=BTUtil.left_idx(root),
                         query_l=query_l, query_r=mid)
        vr = self._query(mid + 1, r, root=BTUtil.right_idx(root),
                         query_l=mid + 1, query_r=query_r)
        return self.key(vl, vr)

    def _update(self, l: int, r: int, root: int, target_idx: int):
        """在以 `root` 为根的线段树中, 更新包含 `target_idx` 的区间, 根代表的区间为 [l...r]."""
        if l == r == target_idx:
            self._t[root] = self._a[l]
            return

        # 区间分为 [l...mid], [mid+1...r]
        mid = (l + r) // 2

        # `target_idx` 只可能在左区间或右区间
        if target_idx <= mid:
            self._update(l, mid, root=BTUtil.left_idx(root), target_idx=target_idx)
        else:
            self._update(mid + 1, r, root=BTUtil.right_idx(root), target_idx=target_idx)
        self._t[root] = self.key(self._t[BTUtil.left_idx(root)],
                                 self._t[BTUtil.right_idx(root)])


class SegmentTreeWithNode:
    """线段树 (节点存储).

    和 `SegmentTree` 区别比较大的地方才有注释.
    """

    def __init__(self, array: list, key: callable):
        self._a = array
        self.key = key
        self.root: Optional[BTNode] = None

    def __len__(self) -> int:
        return len(self._a)

    def __iter__(self) -> Iterator:
        return (n.val for level in BTUtil.levelorder(self.root) for n in level)

    @check_index()
    def __setitem__(self, index: int, value: Any):
        self._a[index] = value
        self._update(0, len(self) - 1, root=self.root, target_idx=index)

    def query(self, l: int, r: int) -> Any:
        if not (0 <= l < len(self) and 0 <= r < len(self) and l <= r):
            raise IndexError
        return self._query(0, len(self) - 1, root=self.root, query_l=l, query_r=r)

    @classmethod
    def from_iterable(cls, iterable: Iterable, key: callable
                      ) -> 'SegmentTreeWithNode':
        array = list(iterable)
        segement = cls(array, key=key)
        segement.root = segement._build(0, len(segement) - 1)
        return segement

    def _build(self, l: int, r: int) -> Optional[BTNode]:
        """构建表示区间 [l...r] 的线段树, 返回构建完的树."""
        if l > r:
            return
        if l == r:
            return BTNode(self._a[l])

        mid = (l + r) // 2
        node_l = self._build(l, mid)
        node_r = self._build(mid + 1, r)
        return BTNode(self.key(node_l.val, node_r.val), node_l, node_r)

    def _query(self, l, r, root: BTNode, query_l, query_r) -> Any:
        if l == query_l and r == query_r:
            return root.val

        mid = (l + r) // 2
        if query_r <= mid:
            return self._query(l, mid, root=root.left,
                               query_l=query_l, query_r=query_r)
        elif query_l >= mid + 1:
            return self._query(mid + 1, r, root=root.right,
                               query_l=query_l, query_r=query_r)

        vl = self._query(l, mid, root=root.left, query_l=query_l, query_r=mid)
        vr = self._query(mid + 1, r, root=root.right, query_l=mid + 1, query_r=query_r)
        return self.key(vl, vr)

    def _update(self, l: int, r: int, root: BTNode, target_idx: int):
        if l == r == target_idx:
            root.val = self._a[l]
            return

        mid = (l + r) // 2
        if target_idx <= mid:
            self._update(l, mid, root=root.left, target_idx=target_idx)
        else:
            self._update(mid + 1, r, root=root.right, target_idx=target_idx)
        root.val = self.key(root.left.val, root.right.val)
