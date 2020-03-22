from structure import MaxHeap


def test_add():
    """按以下顺序添加元素.
    ```
    2   3    3      5      5      5        6
       2   2  1   3  1   3  1   3   4    3   5
                 2      2 0    2 0 1    2 0 1 4
    ```
    """
    heap = MaxHeap()

    heap.add(2)
    assert len(heap) == 1
    assert list(heap) == [2]

    heap.add(3)
    assert len(heap) == 2
    assert list(heap) == [3, 2]

    heap.add(1)
    assert len(heap) == 3
    assert list(heap) == [3, 2, 1]

    heap.add(5)
    assert len(heap) == 4
    assert list(heap) == [5, 3, 1, 2]

    heap.add(0)
    assert len(heap) == 5
    assert list(heap) == [5, 3, 1, 2, 0]

    heap.add(4)
    assert len(heap) == 6
    assert list(heap) == [5, 3, 4, 2, 0, 1]

    heap.add(6)
    assert len(heap) == 7
    assert list(heap) == [6, 3, 5, 2, 0, 1, 4]
