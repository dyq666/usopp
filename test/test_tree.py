from functools import partial
from typing import Callable, List, Optional

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
def bst_arrays() -> List[List[Optional[int]]]:
    """返回一些由平衡二叉树层序遍历的结果 (最大层数: 3).
    1. 空树
    2. 只有根节点
    3. 只有左
    4. 只有右
    5. 第二层只有左
    6. 第二层只有右
    7. 满树
    ```
    N     3      3       3         3           3           3
               1  N    N  5      1   5       1   5       1   5
              0 N        N 6    0 N 4 N     N 2 N 6     0 2 4 6
    ```
    """
    return [
        [],
        [3],
        [3, 1, None, 0],
        [3, None, 5, None, None, None, 6],
        [3, 1, 5, 0, None, 4, None],
        [3, 1, 5, None, 2, None, 6],
        [3, 1, 5, 0, 2, 4, 6],
    ]


class TestBST:

    @pytest.mark.parametrize('f', (BST.add,
                                   BST.add_with_recursion,))
    def test_add(self, f: Callable, bst_arrays: List[List[Optional[int]]]):
        for array in bst_arrays:
            tree = BST()
            for val in array:
                if val is not None:
                    f(tree, val)
            assert BTUtil.is_equal(tree.root, BTNode.from_iterable(array))
            assert len(tree) == sum(1 for i in array if i is not None)

        # 重复元素应该被忽略
        array = bst_arrays[6]
        tree = BST()
        for val in array:
            if val is not None:
                f(tree, val)
                f(tree, val)
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable(array))
        assert len(tree) == sum(1 for i in array if i is not None)

    @pytest.mark.parametrize('f', (BST.remove,
                                   BST.remove_with_recursion,))
    def test_remove(self, f: Callable, bst_arrays: List[List[Optional[int]]]):
        # 从空树中删除.
        tree = BST.from_iteralbe(bst_arrays[0])
        with pytest.raises(IndexError):
            f(tree, 1)

        # 删除叶子节点 (考虑根节点).
        # 根节点
        tree = BST.from_iteralbe(bst_arrays[1])
        # 测试删除不存在的元素
        with pytest.raises(ValueError):
            f(tree, 100)
        f(tree, 3)
        assert len(tree) == 0
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([]))
        # 非根节点
        tree = BST.from_iteralbe(bst_arrays[6])
        f(tree, 6)
        assert len(tree) == 6
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([3, 1, 5, 0, 2, 4]))
        f(tree, 4)
        assert len(tree) == 5
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([3, 1, 5, 0, 2]))

        # 删除只有右子树的节点.
        # 根节点
        tree = BST.from_iteralbe(v for v in bst_arrays[3] if v is not None)
        f(tree, 3)
        assert len(tree) == 2
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([5, None, 6]))
        # 非根节点
        tree = BST.from_iteralbe(v for v in bst_arrays[5] if v is not None)
        f(tree, 5)
        assert len(tree) == 4
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([3, 1, 6, None, 2]))
        f(tree, 1)
        assert len(tree) == 3
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([3, 2, 6]))

        # 删除只有左子树的节点.
        # 根节点
        tree = BST.from_iteralbe(v for v in bst_arrays[2] if v is not None)
        f(tree, 3)
        assert len(tree) == 2
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([1, 0]))
        # 非根节点
        tree = BST.from_iteralbe(v for v in bst_arrays[4] if v is not None)
        f(tree, 1)
        assert len(tree) == 4
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([3, 0, 5, None, None, 4, None]))
        f(tree, 5)
        assert len(tree) == 3
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([3, 0, 4]))

        # 删除有左右子树的节点.
        tree = BST.from_iteralbe(v for v in bst_arrays[6] if v is not None)
        f(tree, 3)
        assert len(tree) == 6
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([4, 1, 5, 0, 2, None, 6]))
        f(tree, 4)
        assert len(tree) == 5
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([5, 1, 6, 0, 2]))
        f(tree, 5)
        assert len(tree) == 4
        assert BTUtil.is_equal(tree.root, BTNode.from_iterable([6, 1, None, 0, 2]))


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
    def test_levelorder_with_none(self, f: Callable, trees: List[BTNode]):
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
