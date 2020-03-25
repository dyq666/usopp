__all__ = (
    'SegmentTree',
    'SegmentTree2',
)

from typing import Any, Iterable

from .tree import BTUtil
from .util import check_index


class SegmentTree:
    """线段树.

    为什么要申请 4N 大小的树来存储 N 个元素 ?

    答: 首先, 树中每一层元素的个数必须是 2 的几次方. 其次, 最后一层的个数减一
    等于之前所有层的个数, 假设我们已知最后一个层个数为 a, 可得整个树的元素个数为
    a + a - 1 ~= 2a, 因而上述问题可变为: 存储 N 个元素, 最后一层的大小是多少 ?
    假设当 N = 8 时, 由于 8 正好等于 2 ** 3, 因而最后一层个数就等于 8,
    最终需要申请 2 * 16 = 16 大小的树. 当 N = 9 时, 需要寻找大于 9 且最近的 2 的几次方,
    此值为 16, 因而最后一层个数等于 16, 最终需要申请 2 * 16 = 32 大小的树.
    在上面这种方式中我们每次都需要计算 log(2, N) 找到一个值, 比较麻烦. 如果我们
    每次都让 N 个元素的最后一行为 2N 个, 就不需要计算 log2 了. 当 N = 8 时,
    8 * 4 > 8 * 2 = 16, 当 N = 9 时, 9 * 4 > 8 * 4 = 32.
    """

    def __init__(self, array: list, merger: callable):
        self._array = array[:]
        self._t = [None for _ in range(len(array) * 4)]
        self._merger = merger

        self._build(0, len(array) - 1, 0)

    def __len__(self) -> int:
        return len(self._array)

    @check_index()
    def __setitem__(self, index: int, value: Any):
        self._array[index] = value
        self._set(0, len(self) - 1, 0, index, value)

    def query(self, l: int, r: int) -> Any:
        """查询 [l...r] 范围的数据."""
        if not (0 <= l < len(self) and 0 <= r < len(self) and l <= r):
            raise IndexError
        return self._query(0, len(self) - 1, l, r, 0)

    def _query(self, l: int, r: int, query_l: int, query_r: int, tree_idx: int) -> Any:
        """在以根为 `tree_idx` 的 [l...r] 的范围中查询, [query_l...query_r] 范围的数据."""
        if l == query_l and r == query_r:
            return self._t[tree_idx]

        # 将范围劈成两半, [l...mid], [mid + 1...r]
        mid = (l + r) // 2
        l_node, r_node = BTUtil.left_idx(tree_idx), BTUtil.right_idx(tree_idx)

        # 如果查询的左索引在中间索引的右边, 那么直接去查右区间.
        if query_l >= mid + 1:
            return self._query(mid + 1, r, query_l, query_r, r_node)
        # 如果查询的右索引在中间索引的左边, 那么直接去查左区间.
        if query_r <= mid:
            return self._query(l, mid, query_l, query_r, l_node)
        # 否则证明, 查询索引横跨左右区间, 因此两边分开找.
        vl = self._query(l, mid, query_l, mid, l_node)
        vr = self._query(mid + 1, r, query_r, mid + 1, r_node)
        return self._merger(vl, vr)

    def _build(self, l: int, r: int, tree_idx: int):
        """构建一课根节点为 `tree_idx` 的线段树, 根节点代表的区间为 [l...r]."""
        # 无效区间
        if l > r:
            return
        # 区间不可再分
        if l == r:
            self._t[tree_idx] = self._array[l]
            return

        mid = (l + r) // 2
        l_node, r_node = BTUtil.left_idx(tree_idx), BTUtil.right_idx(tree_idx)

        # 后续遍历
        self._build(l, mid, l_node)
        self._build(mid + 1, r, r_node)
        self._t[tree_idx] = self._merger(self._t[l_node],
                                         self._t[r_node])

    def _set(self, l: int, r: int, tree_idx: int, target_idx: int, value: Any):
        """在以根节点 `tree_idx` 的 [l...r] 中范围中设置 `target_idx` 的值.

        实际上和 `_build` 逻辑几乎一样, 只不过 `_build` 中要设置所有索引,
        而 `_set` 只用设置 `target_idx` 一个索引.
        """
        if l == r:
            self._t[tree_idx] = value
            return

        # 将区间分为 [l...mid], [mid+1...r]
        mid = (l + r) // 2
        l_node, r_node = BTUtil.left_idx(tree_idx), BTUtil.right_idx(tree_idx)

        # 比较像链表后序遍历, 每个节点都得等后面的所有节点修改过了才能修改.
        if target_idx >= mid + 1:
            self._set(mid + 1, r, r_node, target_idx, value)
        else:
            self._set(l, mid, l_node, target_idx, value)
        self._t[tree_idx] = self._merger(self._t[l_node],
                                         self._t[r_node])


class SegmentTree2:

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

    @classmethod
    def from_iterable(cls, iterable: Iterable, key: callable
                      ) -> 'SegmentTree2':
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
