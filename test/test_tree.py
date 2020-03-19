from functools import partial
from typing import Callable, List

import pytest

from structure import BST, BTNode, BTUtil


@pytest.fixture
def bt_arrays() -> List:
    """由 fixture `trees` 中的树层序遍历后生成的数组."""
    return [
        [1, 2, 3, None, 5],
        [1, 2, None, 9, None],
        [],
        [1, None, 9, None, None, 8, None],
        [1, 2, 3],
        [9, 8, 7, None, 4, 3, None],
    ]


@pytest.fixture
def trees(bt_arrays: List) -> List[BTNode]:
    """返回如下的一些树 (最大层数: 3).
    ```
        1         1      N      1        1       9
      2   3     2   N         N   9    2   3   8   7
     N 5       9 N               8 N          N 4 3 N
    ```
    """
    return [BTNode.from_iterable(a) for a in bt_arrays]


@pytest.fixture
def bst_arrays() -> List:
    """返回如下的一些平衡二叉树 (最大层数: 3).
    ```
        3         9      N     1        2       7
      1   5     2  N         N   9    1   3   3   9
     N 2       1 N              8 N          N 4 8 N
    ```
    """
    return [
        [3, 1, 5, None, 2],
        [9, 2, None, 1, None],
        [],
        [1, None, 9, 8, None],
        [2, 1, 3],
        [7, 3, 9, None, 4, 8, None],
    ]


class TestBST:

    def test_add(self, bst_arrays):
        for array in bst_arrays:
            tree = BST()
            for val in array:
                if val is not None:
                    tree.add(val)
            res = [n and n.val for level in BTUtil.levelorder(tree.root, skip_none=False)
                   for n in level]
            assert res == array
            assert len(tree) == sum(1 for i in array if i is not None)


class TestBTUtil:

    @pytest.mark.parametrize('f', (BTUtil.preorder,
                                   BTUtil.preorder_with_mocked_stack,
                                   BTUtil.preorder_with_recursion,))
    def test_preorder(self, trees: List[BTNode], f: Callable):
        assert list(n.val for n in f(trees[0])) == [1, 2, 5, 3]
        assert list(n.val for n in f(trees[1])) == [1, 2, 9]
        assert list(n.val for n in f(trees[2])) == []
        assert list(n.val for n in f(trees[3])) == [1, 9, 8]
        assert list(n.val for n in f(trees[4])) == [1, 2, 3]
        assert list(n.val for n in f(trees[5])) == [9, 8, 4, 7, 3]

    @pytest.mark.parametrize('f', (partial(BTUtil.preorder, skip_none=False),
                                   BTUtil.preorder_with_mocked_stack_and_none,
                                   BTUtil.preorder_with_recursion_and_none))
    def test_preorder_with_none(self, trees: List[BTNode], f: Callable):
        assert list(n and n.val for n in f(trees[0])) == [1, 2, None, 5, 3]
        assert list(n and n.val for n in f(trees[1])) == [1, 2, 9, None, None]
        assert list(n and n.val for n in f(trees[2])) == []
        assert list(n and n.val for n in f(trees[3])) == [1, None, 9, 8, None]
        assert list(n and n.val for n in f(trees[4])) == [1, 2, 3]
        assert list(n and n.val for n in f(trees[5])) == [9, 8, None, 4, 7, 3, None]

    @pytest.mark.parametrize('f', (BTUtil.inorder,))
    def test_inorder(self, trees: List[BTNode], f: Callable):
        assert list(n.val for n in f(trees[0])) == [2, 5, 1, 3]
        assert list(n.val for n in f(trees[1])) == [9, 2, 1]
        assert list(n.val for n in f(trees[2])) == []
        assert list(n.val for n in f(trees[3])) == [1, 8, 9]
        assert list(n.val for n in f(trees[4])) == [2, 1, 3]
        assert list(n.val for n in f(trees[5])) == [8, 4, 9, 3, 7]

    @pytest.mark.parametrize('f', (BTUtil.postorder,))
    def test_postorder(self, trees: List[BTNode], f: Callable):
        assert list(n.val for n in f(trees[0])) == [5, 2, 3, 1]
        assert list(n.val for n in f(trees[1])) == [9, 2, 1]
        assert list(n.val for n in f(trees[2])) == []
        assert list(n.val for n in f(trees[3])) == [8, 9, 1]
        assert list(n.val for n in f(trees[4])) == [2, 3, 1]
        assert list(n.val for n in f(trees[5])) == [4, 8, 3, 7, 9]

    @pytest.mark.parametrize('f', (BTUtil.levelorder,))
    def test_levelorder(self, trees: List[BTNode], f: Callable):
        assert list(n.val for level in f(trees[0]) for n in level) == [1, 2, 3, 5]
        assert list(n.val for level in f(trees[1]) for n in level) == [1, 2, 9]
        assert list(n.val for level in f(trees[2]) for n in level) == []
        assert list(n.val for level in f(trees[3]) for n in level) == [1, 9, 8]
        assert list(n.val for level in f(trees[4]) for n in level) == [1, 2, 3]
        assert list(n.val for level in f(trees[5]) for n in level) == [9, 8, 7, 4, 3]

    @pytest.mark.parametrize('f', (partial(BTUtil.levelorder, skip_none=False),))
    def test_levelorder(self, trees: List[BTNode], f: Callable):
        assert list(n and n.val for level in f(trees[0]) for n in level) == [1, 2, 3, None, 5]
        assert list(n and n.val for level in f(trees[1]) for n in level) == [1, 2, None, 9, None]
        assert list(n and n.val for level in f(trees[2]) for n in level) == []
        assert list(n and n.val for level in f(trees[3]) for n in level) == [1, None, 9, 8, None]
        assert list(n and n.val for level in f(trees[4]) for n in level) == [1, 2, 3]
        assert list(n and n.val for level in f(trees[5]) for n in level) == [9, 8, 7, None, 4, 3, None]
