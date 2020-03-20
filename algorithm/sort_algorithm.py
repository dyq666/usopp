__all__ = (
    'merge_sort',
    'bubble_sort',
    'insertion_sort',
    'selection_sort',
    'bubble_sort_optimization_1',
)

from typing import Callable

import pytest

from .util import swap_two_ele


def selection_sort(array: list) -> None:
    """选择排序
    思路:
        初始情况下未排序数组长度为 n, 每执行一次操作 (操作为: 从未排序的数组中选出最小值, 放到数组的最前面. ) 长度就-1,
    n-1 次后数组有序.
    """
    len_ = len(array)
    for start_i in range(len_ - 1):
        min_i = start_i
        for finding_i in range(start_i + 1, len_):
            if array[finding_i] < array[min_i]:
                min_i = finding_i
        swap_two_ele(array, start_i, min_i)


def insertion_sort(array: list) -> None:
    """插入排序
    思路:
        从第二个元素开始, 将所有元素向前插入到合适位置 (合适位置: 如果插入元素大于前面某个元素, 那么插入位置为该元素+1,
    如果一个都没有, 则插入元素小于前面所有的元素, 因此插入首位).
    """
    for start_i in range(1, len(array)):
        # 找到插入位置
        insertion_i = 0
        for finding_i in range(start_i - 1, -1, -1):
            if array[start_i] > array[finding_i]:
                insertion_i = finding_i + 1
                break

        # 后移一部分元素后插入
        insertion_value = array[start_i]
        array[insertion_i + 1:start_i + 1] = array[insertion_i:start_i]
        array[insertion_i] = insertion_value


def bubble_sort(array: list) -> None:
    """冒泡排序
    思路:
        执行 n-1 次, 每次从第二个元素到无序数组末尾 (末尾的索引等于 n - 当前的次数),
    将每个元素与前一个元素比较, 按升序排列.
    """
    len_ = len(array)
    for time in range(1, len_):
        for i in range(1, len_ - time + 1):
            if array[i - 1] > array[i]:
                swap_two_ele(array, i - 1, i)


def bubble_sort_optimization_1(array: list) -> None:
    """冒泡排序优化一
    优化:
        如果某次冒泡时无交换操作, 那么剩下数组已是有序的.
    """
    len_ = len(array)
    for time in range(1, len_):
        swaped = False
        for i in range(1, len_ - time + 1):
            if array[i - 1] > array[i]:
                swaped = True
                swap_two_ele(array, i - 1, i)
        if not swaped:
            break


def merge_sort(array: list) -> list:
    """归并排序 (非原地)
    思路:
        将数组二等分, 直到所有子数组的元素个数小于2, 将子数组按拆分过程进行合并,
    合并后的数组需要保证升序.
    """
    # 递归终结条件
    if len(array) <= 1:
        return array

    # 分
    l, r = 0, len(array) - 1
    mid = (l + r) // 2
    l_array = merge_sort(array[l:mid + 1])
    r_array = merge_sort(array[mid + 1:r + 1])

    # 合
    new_array = []
    l_merge_i, r_merge_i = 0, 0
    while l_merge_i < len(l_array) and r_merge_i < len(r_array):
        l_cur_value, r_cur_value = l_array[l_merge_i], r_array[r_merge_i]
        if l_cur_value < r_cur_value:
            l_merge_i += 1
            new_array.append(l_cur_value)
        else:
            r_merge_i += 1
            new_array.append(r_cur_value)
    new_array.extend(l_array[l_merge_i:])
    new_array.extend(r_array[r_merge_i:])
    return new_array


def quick_sort(array: list) -> list:
    """快排 (非原地)
    思路:
        将数组按照某个元素的大小为两部分, 直到所有子数组的元素个数小于2, 将子数组按拆分过程进行合并,
    合并时需要加上分割点.
    """
    # 递归结束条件
    if len(array) <= 1:
        return array

    # 分
    pivot = array.pop()
    less = quick_sort([i for i in array if i <= pivot])
    greater = quick_sort([i for i in array if i > pivot])

    # 合
    return less + [pivot] + greater


# 测试用例参考: http://swtestnextstep.blogspot.com/2013/09/how-to-test-sorting-algorithm.html
@pytest.mark.parametrize(('sort_func', 'in_place'), (
    (merge_sort, False),
    (quick_sort, False),
    (bubble_sort, True),
    (insertion_sort, True),
    (selection_sort, True),
    (bubble_sort_optimization_1, True),
))
@pytest.mark.parametrize(('array', 'sorted_array'), (
    ([], []),
    ([1], [1]),
    ([1, 2, 3], [1, 2, 3]),
    ([3, 2, 1], [1, 2, 3]),
    ([-2, 3, -1, 10], [-2, -1, 3, 10]),
    ([1, 5, 5, 10, 2, 2], [1, 2, 2, 5, 5, 10])
))
def test_sort(array: list, sorted_array: list, sort_func: Callable, in_place: bool) -> None:
    # sort_func 会重复使用 array
    array = array[:]
    if in_place:
        sort_func(array)
        assert array == sorted_array
    else:
        assert sort_func(array) == sorted_array
