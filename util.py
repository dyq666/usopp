__all__ = (
    'PrioQueue', 'check_index', 'merge_sorted_list', 'not_empty',
)

import heapq
from functools import wraps
from typing import Any, Callable, Iterable, Sized, Tuple


class PrioQueue:
    """copy from https://github.com/dyq666/sanji"""

    def __init__(self, asc: bool = True):
        self._queue = []
        self._index = 0
        self._asc = asc

    def __len__(self) -> int:
        return len(self._queue)

    def put(self, priority: int, item: Any):
        priority = priority if self._asc else -priority
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def get(self):
        return heapq.heappop(self._queue)[-1]

    @classmethod
    def from_pairs(cls, pairs: Iterable[Tuple[int, Any]],
                   asc: bool = True) -> 'PrioQueue':
        q = cls(asc)
        for priority, item in pairs:
            q.put(priority, item)
        return q


def check_index(offset: int = 0) -> Callable:
    """在执行数据结构某个方法前检查索引是否有效.

    方法必须满足第一个参数是 `self`, 第二是索引, 同时类必须实现 `__len__`.

    索引的检查范围是 [0, len + offset).
    """
    def deco(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(self: Any, index: int, *args, **kwargs):
            if not (0 <= index < len(self) + offset):
                raise IndexError
            return f(self, index, *args, **kwargs)

        return wrapper

    return deco


def merge_sorted_list(a1: list, a2: list) -> Iterable:
    """copy from https://github.com/dyq666/sanji"""
    idx1, idx2 = 0, 0

    for _ in range(len(a1) + len(a2)):
        # 如果某个数组遍历结束了, 就用无穷大代替当前数组的值.
        v1 = a1[idx1] if idx1 < len(a1) else float('inf')
        v2 = a2[idx2] if idx2 < len(a2) else float('inf')
        if v1 < v2:
            idx1 += 1
        else:
            idx2 += 1
        yield min(v1, v2)


def not_empty(f: Callable) -> Callable:
    """在执行数据结构某个方法前检查数据结构是否为空."""
    @wraps(f)
    def wrapper(self: Sized, *args, **kwargs):
        if len(self) == 0:
            raise IndexError
        return f(self, *args, **kwargs)

    return wrapper
