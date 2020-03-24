__all__ = (
    'MaxHeap',
)

from typing import Any, Iterable, Optional

from .tree import BTUtil
from .util import not_empty


class MaxHeap:
    """最大堆.

    函数命名和 `import heapq` 保持一致.

    可使用 LeetCode 347 测试.
    """

    def __init__(self, data: Optional[list] = None):
        """注意如果传入 `data` 必须保证 `data` 已经是一个最大堆了.

        如果不能保证则应该使用 `heapify`.
        """
        self._data = [] if data is None else data[:]

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterable:
        return iter(self._data)

    def push(self, value: Any):
        """添加元素.

        先将元素放到末尾, 再升上去.
        """
        self._data.append(value)
        self._sift_up(len(self) - 1)

    @not_empty
    def pop(self) -> Any:
        """删除元素.

        头和尾互换, 换完之后, 尾弹出, 头下降.
        """
        d = self._data
        d[0], d[-1] = d[-1], d[0]
        max_ = d.pop()
        self._sift_down(0)
        return max_

    @not_empty
    def replace(self, value: Any) -> Any:
        """先 `pop` 首元素, 再 `push` 一个元素.

        :) 实际上这个方法可以叫做 `poppush`!
        """
        max_ = self._data[0]
        self._data[0] = value
        self._sift_down(0)
        return max_

    def pushpop(self, value: Any) -> Any:
        """先 `push` 一个元素, 再 `pop` 首元素."""
        if len(self) == 0 or value >= self._data[0]:
            return value

        # 当 `value < max_` 时, 和先 `pop` 后 `push` 就是一样的
        return self.replace(value)

    def _sift_up(self, index: int):
        """上升元素."""
        d = self._data
        # 如果没上升到头并且比父亲大, 则继续上升
        while index > 0 and d[index] > d[BTUtil.parent_idx(index)]:
            parent = BTUtil.parent_idx(index)
            d[index], d[parent] = d[parent], d[index]
            index = parent

    def _sift_down(self, index: int):
        """下降元素."""
        d = self._data
        l, r = BTUtil.left_idx(index), BTUtil.right_idx(index)
        # 当左 >= len 时, 等价于 `index` 没有左, 由于右 = 左 + 1, 因而也没有右,
        # 所以此时 `index` 是叶子, 叶子无法继续下降.
        while l < len(self):
            # 如果有右节点, 则从左右中选择一个大的.
            if r < len(self):
                child = l if d[l] > d[r] else r
            else:
                child = l

            # 父比孩子中最大的还大, 不需要下降了.
            if d[index] >= d[child]:
                break
            d[child], d[index] = d[index], d[child]
            index = child
            l, r = BTUtil.left_idx(index), BTUtil.right_idx(index)

    @classmethod
    def heapify(cls, data: list) -> 'MaxHeap':
        """使任意排序的数组转换成堆.

        从最后一个非叶子节点到第一个节点逐个下降 (实际上从最后一个
        节点开始下降也是可以的, 只不过叶子节点下降等于什么都不干).

        heapify 的时间复杂度是 O(N) !
        """
        data = data[:]
        if len(data) < 2:
            return cls(data)

        last = BTUtil.parent_idx(len(data) - 1)
        heap = cls(data)
        for i in range(last, -1, -1):
            heap._sift_down(i)
        return heap
