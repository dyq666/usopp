from functools import partial
from typing import Callable, List

import pytest

from structure import BST, BTNode, BTUtil


@pytest.fixture
def trees() -> List[BTNode]:
    """返回如下的一些树 (最大层数: 3).
    ```
        1         1      N      1        1       9
      2   3     2   N         N   9    2   3   8   7
     N 5       9 N               8 N          N 4 3 N
    ```
    """
    return [
        BTNode.from_iterable([1, 2, 3, None, 5]),
        BTNode.from_iterable([1, 2, None, 9, None]),
        BTNode.from_iterable([]),
        BTNode.from_iterable([1, None, 9, None, None, 8, None]),
        BTNode.from_iterable([1, 2, 3]),
        BTNode.from_iterable([9, 8, 7, None, 4, 3, None]),
    ]


@pytest.fixture
def bst_arrays() -> List[List]:
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
        [1, None, 9, None, None, 8, None],
        [2, 1, 3],
        [7, 3, 9, None, 4, 8, None],
    ]


class TestBST:

    @pytest.mark.parametrize('f', (BST.add, BST.add_with_recursion,
                                   BST.add_with_recursion2))
    def test_add(self, f: Callable, bst_arrays: List[List]):
        for array in bst_arrays:
            tree = BST()
            for val in array:
                if val is not None:
                    f(tree, val)
            assert BTUtil.is_equal(tree.root, BTNode.from_iterable(array))
            assert len(tree) == sum(1 for i in array if i is not None)

        # 重复元素应该被忽略
        array = bst_arrays[0]
        tree = BST()
        for val in array:
            if val is not None:
                f(tree, val)
                f(tree, val)
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable(array))
        assert len(tree) == sum(1 for i in array if i is not None)

    @pytest.mark.parametrize('f', (BST.pop_max, BST.pop_max_with_recursion))
    def test_pop_max(self, f: Callable):
        """
        1. 从空树中删除.

        2. 删除只有右节点的树.
        ```
           0
          N  1
            N 2
        ```

        3. 删除三层满二叉树.
        ```
            3
          1   5
         0 2 4 6
        ```
        """
        # 1
        tree = BST()
        with pytest.raises(IndexError):
            f(tree)

        # 2
        tree = BST()
        for i in range(3):
            tree.add(i)
        assert 2 == f(tree)
        assert len(tree) == 2
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([0, None, 1]))
        assert 1 == f(tree)
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([0]))
        assert 0 == f(tree)
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([]))

        # 3
        tree = BST()
        for i in [3, 1, 5, 0, 2, 4, 6]:
            tree.add(i)
        assert 6 == f(tree)
        assert len(tree) == 6
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([3, 1, 5, 0, 2, 4]))
        assert 5 == f(tree)
        assert len(tree) == 5
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([3, 1, 4, 0, 2]))
        assert 4 == f(tree)
        assert len(tree) == 4
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([3, 1, None, 0, 2]))
        assert 3 == f(tree)
        assert len(tree) == 3
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([1, 0, 2]))
        assert 2 == f(tree)
        assert len(tree) == 2
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([1, 0]))
        assert 1 == f(tree)
        assert len(tree) == 1
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([0]))
        assert 0 == f(tree)
        assert len(tree) == 0
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([]))

    @pytest.mark.parametrize('f', (BST.pop_min, BST.pop_min_with_recursion))
    def test_pop_min(self, f: Callable):
        """
        1. 从空树中删除.

        2. 删除只有右节点的树.
        ```
           0
          N  1
            N 2
        ```

        3. 删除三层满二叉树.
        ```
            3
          1   5
         0 2 4 6
        ```
        """
        # 1
        tree = BST()
        with pytest.raises(IndexError):
            tree.pop_min()

        # 2
        tree = BST()
        for i in range(3):
            tree.add(i)
        assert 0 == f(tree)
        assert len(tree) == 2
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([1, None, 2]))
        assert 1 == f(tree)
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([2]))
        assert 2 == f(tree)
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([]))

        # 3
        tree = BST()
        for i in [3, 1, 5, 0, 2, 4, 6]:
            tree.add(i)
        assert 0 == f(tree)
        assert len(tree) == 6
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([3, 1, 5, None, 2, 4, 6]))
        assert 1 == f(tree)
        assert len(tree) == 5
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([3, 2, 5, None, None, 4, 6]))
        assert 2 == f(tree)
        assert len(tree) == 4
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([3, None, 5, None, None, 4, 6]))
        assert 3 == f(tree)
        assert len(tree) == 3
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([5, 4, 6]))
        assert 4 == f(tree)
        assert len(tree) == 2
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([5, None, 6]))
        assert 5 == f(tree)
        assert len(tree) == 1
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([6]))
        assert 6 == f(tree)
        assert len(tree) == 0
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([]))


class TestBTUtil:

    @pytest.mark.parametrize('f', (BTUtil.preorder,
                                   BTUtil.preorder_with_mocked_stack,
                                   BTUtil.preorder_with_recursion,))
    def test_preorder(self, f: Callable, trees: List[BTNode]):
        assert list(n.val for n in f(trees[0])) == [1, 2, 5, 3]
        assert list(n.val for n in f(trees[1])) == [1, 2, 9]
        assert list(n.val for n in f(trees[2])) == []
        assert list(n.val for n in f(trees[3])) == [1, 9, 8]
        assert list(n.val for n in f(trees[4])) == [1, 2, 3]
        assert list(n.val for n in f(trees[5])) == [9, 8, 4, 7, 3]

    @pytest.mark.parametrize('f', (partial(BTUtil.preorder, skip_none=False),
                                   BTUtil.preorder_with_mocked_stack_and_none,
                                   BTUtil.preorder_with_recursion_and_none))
    def test_preorder_with_none(self, f: Callable, trees: List[BTNode]):
        assert list(n and n.val for n in f(trees[0])) == [1, 2, None, 5, 3]
        assert list(n and n.val for n in f(trees[1])) == [1, 2, 9, None, None]
        assert list(n and n.val for n in f(trees[2])) == []
        assert list(n and n.val for n in f(trees[3])) == [1, None, 9, 8, None]
        assert list(n and n.val for n in f(trees[4])) == [1, 2, 3]
        assert list(n and n.val for n in f(trees[5])) == [9, 8, None, 4, 7, 3, None]

    @pytest.mark.parametrize('f', (BTUtil.inorder,))
    def test_inorder(self, f: Callable, trees: List[BTNode]):
        assert list(n.val for n in f(trees[0])) == [2, 5, 1, 3]
        assert list(n.val for n in f(trees[1])) == [9, 2, 1]
        assert list(n.val for n in f(trees[2])) == []
        assert list(n.val for n in f(trees[3])) == [1, 8, 9]
        assert list(n.val for n in f(trees[4])) == [2, 1, 3]
        assert list(n.val for n in f(trees[5])) == [8, 4, 9, 3, 7]

    @pytest.mark.parametrize('f', (BTUtil.postorder,))
    def test_postorder(self, f: Callable, trees: List[BTNode]):
        assert list(n.val for n in f(trees[0])) == [5, 2, 3, 1]
        assert list(n.val for n in f(trees[1])) == [9, 2, 1]
        assert list(n.val for n in f(trees[2])) == []
        assert list(n.val for n in f(trees[3])) == [8, 9, 1]
        assert list(n.val for n in f(trees[4])) == [2, 3, 1]
        assert list(n.val for n in f(trees[5])) == [4, 8, 3, 7, 9]

    @pytest.mark.parametrize('f', (BTUtil.levelorder,))
    def test_levelorder(self, f: Callable, trees: List[BTNode]):
        assert list(n.val for level in f(trees[0]) for n in level) == [1, 2, 3, 5]
        assert list(n.val for level in f(trees[1]) for n in level) == [1, 2, 9]
        assert list(n.val for level in f(trees[2]) for n in level) == []
        assert list(n.val for level in f(trees[3]) for n in level) == [1, 9, 8]
        assert list(n.val for level in f(trees[4]) for n in level) == [1, 2, 3]
        assert list(n.val for level in f(trees[5]) for n in level) == [9, 8, 7, 4, 3]

    @pytest.mark.parametrize('f', (partial(BTUtil.levelorder, skip_none=False),))
    def test_levelorder(self, f: Callable, trees: List[BTNode]):
        assert list(n and n.val for level in f(trees[0]) for n in level) == [1, 2, 3, None, 5]
        assert list(n and n.val for level in f(trees[1]) for n in level) == [1, 2, None, 9, None]
        assert list(n and n.val for level in f(trees[2]) for n in level) == []
        assert list(n and n.val for level in f(trees[3]) for n in level) == [1, None, 9, 8, None]
        assert list(n and n.val for level in f(trees[4]) for n in level) == [1, 2, 3]
        assert list(n and n.val for level in f(trees[5]) for n in level) == [9, 8, 7, None, 4, 3, None]

    def test_is_equal(self):
        f = BTUtil.is_equal
        gen = BTNode.from_iterable
        assert f(gen([]), gen([]))
        # 第一个树 5 是 2 的右节点, 第二个则是左节点
        assert not f(gen([1, 2, 3, None, 5]), gen([1, 2, 3, 5]))
        assert f(gen([1, 2, 3, None, 5]), gen([1, 2, 3, None, 5]))
