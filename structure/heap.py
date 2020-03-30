__all__ = (
    'MaxHeap',
)

from typing import Any, Iterable, Iterator, Optional

from .tree import BTUtil
from .util import not_empty


class MaxHeap:
    """最大堆.

    函数命名和标准库中的 `heapq` 保持一致.

    可在 LeetCode 347 中测试本数据结构.
    """

    def __init__(self, array: Optional[list] = None):
        self._a = [] if array is None else array

    def __len__(self) -> int:
        return len(self._a)

    def __iter__(self) -> Iterator:
        return iter(self._a)

    @not_empty
    def pop(self) -> Any:
        """弹出最大值.

        是如何想到这种方式 ?

        答: 由于底层是一个 list, list 从末尾弹出元素是 O(1) 的, 因此先将
           最大值和末尾元素互换, 让最大值从末尾弹出, 再想办法让 list 维持最大堆的特性.
        """
        self._a[0], self._a[-1] = self._a[-1], self._a[0]
        max_ = self._a.pop()
        self._sift_down(0)
        return max_

    def push(self, value: Any):
        """添加元素.

        是如何想到这种方式 ?

        答: 由于底层是一个 list, list 从末尾添加元素是 O(1) 的, 因此先将
           元素放到末尾, 再想办法让 list 维持最大堆的特性.
        """
        self._a.append(value)
        self._sift_up(len(self) - 1)

    def pushpop(self, value: Any) -> Any:
        """等于先 `push` 一个元素, 再 `pop` 首元素.

        和 `replace` 的区别是 ?

        答: 当 `push` 的元素大于堆中最大值时, `pop` 的也会是这个元素,
           因此堆不需要改变.
        """
        if len(self) == 0 or value >= self._a[0]:
            return value

        return self.replace(value)

    @not_empty
    def replace(self, value: Any) -> Any:
        """等价于先 `pop` 首元素, 再 `push` 一个元素.

        :) 实际上这个方法可以叫做 `poppush`!
        """
        max_ = self._a[0]
        self._a[0] = value
        self._sift_down(0)
        return max_

    def _sift_up(self, index: int):
        """上浮元素."""
        # 没上浮到根 (0 为根), 且比父大, 则上浮.
        while index > 0 and self._a[index] > self._a[BTUtil.parent_idx(index)]:
            parent = BTUtil.parent_idx(index)
            self._a[index], self._a[parent] = self._a[parent], self._a[index]
            index = parent

    def _sift_down(self, index: int):
        """下沉元素."""
        l, r = BTUtil.left_idx(index), BTUtil.right_idx(index)
        # 当左 >= len 时, 等价于 `index` 没有左, 由于右 = 左 + 1, 因而也没有右,
        # 所以此时 `index` 是叶子, 叶子无法继续下沉.
        while l < len(self):
            # 如果有右节点, 则从左右中选择一个大的.
            if r < len(self):
                child = l if self._a[l] > self._a[r] else r
            else:
                child = l

            # 父比孩子中最大的还大, 不需要下沉了.
            if self._a[index] >= self._a[child]:
                break
            self._a[child], self._a[index] = self._a[index], self._a[child]
            index = child
            l, r = BTUtil.left_idx(index), BTUtil.right_idx(index)

    @classmethod
    def heapify(cls, array: Iterable) -> 'MaxHeap':
        """使任意排序的数组转换成堆.

        时间复杂度是 O(N) (具体原因请参考网上资料) !
        """
        array = list(array)
        # 长度 < 2 的数组已经是最大堆了
        if len(array) < 2:
            return cls(array)

        heap = cls(array)
        # 从最后一个非叶子到根逐个下沉
        for i in range(BTUtil.parent_idx(len(array) - 1), -1, -1):
            heap._sift_down(i)
        return heap
