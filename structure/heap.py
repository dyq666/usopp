__all__ = (
    'MaxHeap',
)

from typing import Any, Iterable, Tuple

from .util import not_empty


class MaxHeap:
    """最大堆."""

    def __init__(self):
        self._data = []

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

    def _sift_up(self, index: int):
        """上升元素."""
        d = self._data
        while index > 0:
            parent = self.parent_idx(index)
            # 孩子节点小于父节点就终止
            if d[index] < d[parent]:
                return
            d[index], d[parent] = d[parent], d[index]
            index = parent

    def _sift_down(self, index: int):
        """下降元素."""
        d = self._data
        l, r = self.child_idxes(index)
        # 这个循环条件等价于 `index` 不是叶子节点
        while l < len(self) or r < len(self):
            # 从孩子中找到最大值
            vl = d[l] if l < len(self) else float('-inf')
            vr = d[r] if r < len(self) else float('-inf')
            # 父节点比两个孩子节点都大, 就终止
            if max(d[index], vl, vr) == d[index]:
                break

            child = l if vl > vr else r
            d[child], d[index] = d[index], d[child]
            index = child
            l, r = self.child_idxes(index)

    @staticmethod
    def child_idxes(index: int) -> Tuple[int, int]:
        """获取节点的孩子索引.

        如何推到出父节点和孩子节点之间索引的关系 ?

        答: 根据下图中树和数组的关系, 可以推出索引之间的转换公式.
        ```
             0          [0,
           1   2    ->   1, 2
          3 4 5 6        3, 4, 5, 6]
        ```

        0 -> 1, 2
        1 -> 3, 4
        2 -> 5, 6
        ...
        n -> 2 * n + 1, 2 * n + 2

        1 -> 0
        2 -> 0
        3 -> 1
        4 -> 1
        ...
        n -> (n - 1) // 2
        """
        return index * 2 + 1, index * 2 + 2

    @staticmethod
    def parent_idx(index: int) -> int:
        """获取节点的父索引."""
        if index == 0:
            raise ValueError
        return (index - 1) // 2
