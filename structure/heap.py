__all__ = (
    'MaxHeap',
)

from typing import Tuple


class MaxHeap:
    """最大堆.

    如何推到出父节点和孩子节点之间索引的关系 ?

    答: TODO 完成此问题
    """

    def __init__(self):
        self._size = 0
        self._array = []

    def __len__(self) -> int:
        return self._size

    @staticmethod
    def child_idxes(index: int) -> Tuple[int, int]:
        return index * 2 + 1, index * 2 + 2

    @staticmethod
    def parent_idx(index: int) -> int:
        if index == 0:
            raise ValueError
        return (index - 1) // 2
