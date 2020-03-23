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

    heap.push(2)
    assert len(heap) == 1
    assert list(heap) == [2]

    heap.push(3)
    assert len(heap) == 2
    assert list(heap) == [3, 2]

    heap.push(1)
    assert len(heap) == 3
    assert list(heap) == [3, 2, 1]

    heap.push(5)
    assert len(heap) == 4
    assert list(heap) == [5, 3, 1, 2]

    heap.push(0)
    assert len(heap) == 5
    assert list(heap) == [5, 3, 1, 2, 0]

    heap.push(4)
    assert len(heap) == 6
    assert list(heap) == [5, 3, 4, 2, 0, 1]

    heap.push(6)
    assert len(heap) == 7
    assert list(heap) == [6, 3, 5, 2, 0, 1, 4]


def test_pop():
    """按以下倒序删除元素.
    ```
       6        5       4       3       2      1    0
     3   5    3   4   3   1   2   1   0  1   0
    2 0 1 4  2 0 1   2 0     0
    ```
    """
    heap = MaxHeap()
    for i in [6, 3, 5, 2, 0, 1, 4]:
        heap.push(i)

    assert 6 == heap.pop()
    assert len(heap) == 6
    assert list(heap) == [5, 3, 4, 2, 0, 1]

    assert 5 == heap.pop()
    assert len(heap) == 5
    assert list(heap) == [4, 3, 1, 2, 0]

    assert 4 == heap.pop()
    assert len(heap) == 4
    assert list(heap) == [3, 2, 1, 0]

    assert 3 == heap.pop()
    assert len(heap) == 3
    assert list(heap) == [2, 0, 1]

    assert 2 == heap.pop()
    assert len(heap) == 2
    assert list(heap) == [1, 0]

    assert 1 == heap.pop()
    assert len(heap) == 1
    assert list(heap) == [0]

    assert 0 == heap.pop()
    assert len(heap) == 0
    assert list(heap) == []

    with pytest.raises(IndexError):
        heap.pop()


def test_pushpop_and_replace():
    # 空
    with pytest.raises(IndexError):
        MaxHeap().replace(1)
    assert 1 == MaxHeap().pushpop(1)

    # 比较二者放入一个比堆最大值还大的元素
    heap = MaxHeap()
    for i in range(8, 5, -1):
        heap.push(i)
    assert 9 == heap.pushpop(9)
    assert list(heap) == [8, 7, 6]
    assert 8 == heap.replace(9)
    assert list(heap) == [9, 7, 6]

    # 比较二者放入一个小于堆最大值的元素
    heap = MaxHeap()
    for i in range(8, 5, -1):
        heap.push(i)
    assert 8 == heap.replace(4)
    assert list(heap) == [7, 4, 6]
    heap = MaxHeap()
    for i in range(8, 5, -1):
        heap.push(i)
    assert 8 == heap.pushpop(4)
    assert list(heap) == [7, 4, 6]
