import operator
from typing import List

import pytest

from structure import SegmentTree, SegmentTreeWithNode


@pytest.fixture
def segement_arrays() -> List[List[int]]:
    """空, 奇数个, 偶数个."""
    return [
        [],
        [1, 4, 8],
        [1, 2, 5, 9],
    ]


class TestSegmentTree:

    @pytest.mark.parametrize('f', (SegmentTree.from_iterable,
                                   SegmentTreeWithNode.from_iterable,))
    def test_build(self, f: callable, segement_arrays: List[List[int]]):
        arrays = segement_arrays
        assert list(f(arrays[0], key=operator.add)) == []
        assert list(f(arrays[1], key=operator.add)) == [13, 5, 8, 1, 4]
        assert list(f(arrays[2], key=operator.add)) == [17, 3, 14, 1, 2, 5, 9]
        assert list(f(arrays[0], key=operator.sub)) == []
        assert list(f(arrays[1], key=operator.sub)) == [-11, -3, 8, 1, 4]
        assert list(f(arrays[2], key=operator.sub)) == [3, -1, -4, 1, 2, 5, 9]

    @pytest.mark.parametrize('f', (SegmentTree.from_iterable,
                                   SegmentTreeWithNode.from_iterable,))
    def test_update(self, f: callable, segement_arrays: List[List[int]]):
        arrays = segement_arrays

        tree = f(arrays[0], key=operator.add)
        with pytest.raises(IndexError):
            tree[0] = 1
        with pytest.raises(IndexError):
            tree[-1] = 1
        tree = f(arrays[0], key=operator.sub)
        with pytest.raises(IndexError):
            tree[0] = 1
        with pytest.raises(IndexError):
            tree[-1] = 1

        tree = f(arrays[1], key=operator.add)
        tree[0] = 10
        assert list(tree) == [22, 14, 8, 10, 4]
        tree = f(arrays[1], key=operator.sub)
        tree[0] = 10
        assert list(tree) == [-2, 6, 8, 10, 4]

        tree = f(arrays[2], key=operator.add)
        tree[0] = 10
        assert list(tree) == [26, 12, 14, 10, 2, 5, 9]
        tree = f(arrays[2], key=operator.sub)
        tree[0] = 10
        assert list(tree) == [12, 8, -4, 10, 2, 5, 9]

    @pytest.mark.parametrize('f', (SegmentTree.from_iterable,
                                   SegmentTreeWithNode.from_iterable,))
    def test_query(self, f: callable, segement_arrays: List[List[int]]):
        arrays = segement_arrays

        tree = f(arrays[0], key=operator.add)
        with pytest.raises(IndexError):
            tree.query(0, 0)

        tree = f(arrays[1], key=operator.add)
        with pytest.raises(IndexError):
            tree.query(-1, 0)
        with pytest.raises(IndexError):
            tree.query(0, -1)
        with pytest.raises(IndexError):
            tree.query(2, 1)
        assert tree.query(0, 0) == 1
        assert tree.query(0, 1) == 5
        assert tree.query(0, 2) == 13
        assert tree.query(1, 2) == 12
        tree = f(arrays[1], key=operator.sub)
        assert tree.query(0, 0) == 1
        assert tree.query(0, 1) == -3
        assert tree.query(0, 2) == -11
        assert tree.query(1, 2) == -4

        tree = f(arrays[2], key=operator.add)
        assert tree.query(0, 0) == 1
        assert tree.query(0, 1) == 3
        assert tree.query(0, 2) == 8
        assert tree.query(0, 3) == 17
        assert tree.query(1, 2) == 7
        assert tree.query(1, 3) == 16
        assert tree.query(2, 3) == 14
        tree = f(arrays[2], key=operator.sub)
        assert tree.query(0, 0) == 1
        assert tree.query(0, 1) == -1
        assert tree.query(0, 2) == -6
        assert tree.query(0, 3) == 3
        assert tree.query(1, 2) == -3
        assert tree.query(1, 3) == 6
        assert tree.query(2, 3) == -4
