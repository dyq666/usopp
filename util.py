from typing import Iterable


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
