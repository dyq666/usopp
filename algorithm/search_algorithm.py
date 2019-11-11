__all__ = (
    'binary_search',
)

import pytest


def binary_search(array, target):
    l, r = 0, len(array) - 1

    while l <= r:
        mid = (l + r) // 2
        mid_value = array[mid]
        if mid_value == target:
            return mid
        elif mid_value < target:
            l = mid + 1
        else:
            r = mid - 1

    return -1


@pytest.mark.parametrize(('array', 'target', 'target_index'), (
    ([], 10, -1),
    ([1], 1, 0),
    ([1], 2, -1),
    ([-1, 3, 4], 4, 2),
    ([-1, 3, 4], -1, 0),
))
def test_search(array, target, target_index):
    assert target_index == binary_search(array, target)
