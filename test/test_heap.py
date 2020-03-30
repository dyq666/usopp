import pytest

from structure import MaxHeap


def test_push():
    """按以下顺序添加元素.
    ```
    2   3    3      5      5      5        6
       2   2  1   3  1   3  1   3   4    3   5
                 2      2 0    2 0 1    2 0 1 4
    ```
    """
    heap = MaxHeap()
    steps = {
        2: [2],
        3: [3, 2],
        1: [3, 2, 1],
        5: [5, 3, 1, 2],
        0: [5, 3, 1, 2, 0],
        4: [5, 3, 4, 2, 0, 1],
        6: [6, 3, 5, 2, 0, 1, 4],
    }

    for val, array in steps.items():
        heap.push(val)
        assert list(heap) == array


def test_pop():
    """按以下顺序删除元素.
    ```
       6        5       4       3       2      1    0
     3   5    3   4   3   1   2   1   0  1   0
    2 0 1 4  2 0 1   2 0     0
    ```
    """
    heap = MaxHeap([6, 3, 5, 2, 0, 1, 4])
    steps = {
        6: [5, 3, 4, 2, 0, 1],
        5: [4, 3, 1, 2, 0],
        4: [3, 2, 1, 0],
        3: [2, 0, 1],
        2: [1, 0],
        1: [0],
        0: [],
    }

    for val, array in steps.items():
        assert val == heap.pop()
        assert list(heap) == array

    with pytest.raises(IndexError):
        heap.pop()


def test_pushpop_and_replace():
    # 空堆时, pushpop 行, replace 不行
    with pytest.raises(IndexError):
        MaxHeap().replace(1)
    assert 1 == MaxHeap().pushpop(1)

    # 放入一个比堆最大值还大的元素, pushpop 后, 堆不变, replace 后, 堆变.
    heap = MaxHeap([8, 7, 6])
    assert 9 == heap.pushpop(9)
    assert list(heap) == [8, 7, 6]
    assert 8 == heap.replace(9)
    assert list(heap) == [9, 7, 6]

    # # 放入一个比堆最大值小的元素, pushpop 后, 堆变, replace 后, 堆也变.
    heap = MaxHeap([8, 7, 6])
    assert 8 == heap.replace(4)
    assert list(heap) == [7, 4, 6]
    heap = MaxHeap([8, 7, 6])
    assert 8 == heap.pushpop(4)
    assert list(heap) == [7, 4, 6]


def test_heapify():
    # 长度 < 2 的数组已经是最大堆了
    assert list(MaxHeap.heapify([])) == []
    assert list(MaxHeap.heapify([2])) == [2]

    # 奇数 / 偶数
    assert list(MaxHeap.heapify([2, 3, 1, 4])) == [4, 3, 1, 2]
    assert list(MaxHeap.heapify([0, 4, 3, 2, 1])) == [4, 2, 3, 0, 1]
