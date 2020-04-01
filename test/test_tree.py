from typing import List, Optional

import pytest

from structure import BST, BTNode, BTUtil


@pytest.fixture
def trees(bst_arrays: List[List[Optional[int]]]) -> List[BTNode]:
    """返回一些树 (最大层数: 3)."""
    return [BTUtil.gen_tree(a) for a in bst_arrays]


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
    def test_add(self, f: callable, bst_arrays: List[List[Optional[int]]]):
        for array in bst_arrays:
            tree = BST()
            for val in array:
                if val is not None:
                    f(tree, val)
            assert BTUtil.is_equal(tree._root, BTUtil.gen_tree(array))
            assert len(tree) == sum(1 for i in array if i is not None)
            assert BST.is_bst(tree._root)

        # 重复元素应该被忽略
        array = bst_arrays[6]
        tree = BST()
        for val in array:
            if val is not None:
                f(tree, val)
                f(tree, val)
        assert BTUtil.is_equal(tree._root, BTUtil.gen_tree(array))
        assert len(tree) == sum(1 for i in array if i is not None)
        assert BST.is_bst(tree._root)

    @pytest.mark.parametrize('f', (BST.remove,
                                   BST.remove_with_recursion,))
    def test_remove(self, f: callable, bst_arrays: List[List[Optional[int]]]):
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
        assert BTUtil.is_equal(tree._root, BTUtil.gen_tree([]))
        assert BST.is_bst(tree._root)
        # 非根节点
        tree = BST.from_iteralbe(bst_arrays[6])
        f(tree, 6)
        assert len(tree) == 6
        assert BTUtil.is_equal(tree._root, BTUtil.gen_tree([3, 1, 5, 0, 2, 4]))
        f(tree, 4)
        assert len(tree) == 5
        assert BTUtil.is_equal(tree._root, BTUtil.gen_tree([3, 1, 5, 0, 2]))
        assert BST.is_bst(tree._root)

        # 删除只有右子树的节点.
        # 根节点
        tree = BST.from_iteralbe(v for v in bst_arrays[3] if v is not None)
        f(tree, 3)
        assert len(tree) == 2
        assert BTUtil.is_equal(tree._root, BTUtil.gen_tree([5, None, 6]))
        assert BST.is_bst(tree._root)
        # 非根节点
        tree = BST.from_iteralbe(v for v in bst_arrays[5] if v is not None)
        f(tree, 5)
        assert len(tree) == 4
        assert BTUtil.is_equal(tree._root, BTUtil.gen_tree([3, 1, 6, None, 2]))
        f(tree, 1)
        assert len(tree) == 3
        assert BTUtil.is_equal(tree._root, BTUtil.gen_tree([3, 2, 6]))
        assert BST.is_bst(tree._root)

        # 删除只有左子树的节点.
        # 根节点
        tree = BST.from_iteralbe(v for v in bst_arrays[2] if v is not None)
        f(tree, 3)
        assert len(tree) == 2
        assert BTUtil.is_equal(tree._root, BTUtil.gen_tree([1, 0]))
        assert BST.is_bst(tree._root)
        # 非根节点
        tree = BST.from_iteralbe(v for v in bst_arrays[4] if v is not None)
        f(tree, 1)
        assert len(tree) == 4
        assert BTUtil.is_equal(tree._root, BTUtil.gen_tree([3, 0, 5, None, None, 4, None]))
        f(tree, 5)
        assert len(tree) == 3
        assert BTUtil.is_equal(tree._root, BTUtil.gen_tree([3, 0, 4]))
        assert BST.is_bst(tree._root)

        # 删除有左右子树的节点.
        tree = BST.from_iteralbe(v for v in bst_arrays[6] if v is not None)
        f(tree, 3)
        assert len(tree) == 6
        assert BTUtil.is_equal(tree._root, BTUtil.gen_tree([4, 1, 5, 0, 2, None, 6]))
        assert BST.is_bst(tree._root)
        f(tree, 4)
        assert len(tree) == 5
        assert BTUtil.is_equal(tree._root, BTUtil.gen_tree([5, 1, 6, 0, 2]))
        assert BST.is_bst(tree._root)
        f(tree, 5)
        assert len(tree) == 4
        assert BTUtil.is_equal(tree._root, BTUtil.gen_tree([6, 1, None, 0, 2]))
        assert BST.is_bst(tree._root)

    def test_get_and_contains(self, bst_arrays: List[List[Optional[int]]]):
        tree = BST.from_iteralbe(bst_arrays[6])
        assert tree.get(7) is None
        assert tree.get(6).key == 6
        assert tree.get(7, 100) == 100

        assert 7 not in tree
        assert 6 in tree


class TestBTUtil:

    @pytest.mark.parametrize('f', (BTUtil.preorder,
                                   BTUtil.preorder_with_mocked_stack,
                                   BTUtil.preorder_with_recursion,))
    def test_preorder(self, f: callable, trees: List[BTNode]):
        items = (
            (trees[0], []),
            (trees[1], [3]),
            (trees[2], [3, 1, 0]),
            (trees[3], [3, 5, 6]),
            (trees[4], [3, 1, 0, 5, 4]),
            (trees[5], [3, 1, 2, 5, 6]),
            (trees[6], [3, 1, 0, 2, 5, 4, 6]),
        )
        for tree, res in items:
            assert list(n.key for n in f(tree)) == res

    def test_inorder(self, trees: List[BTNode]):
        items = (
            (trees[0], []),
            (trees[1], [3]),
            (trees[2], [0, 1, 3]),
            (trees[3], [3, 5, 6]),
            (trees[4], [0, 1, 3, 4, 5]),
            (trees[5], [1, 2, 3, 5, 6]),
            (trees[6], [0, 1, 2, 3, 4, 5, 6]),
        )
        for tree, res in items:
            assert list(n.key for n in BTUtil.inorder(tree)) == res

    def test_postorder(self, trees: List[BTNode]):
        items = (
            (trees[0], []),
            (trees[1], [3]),
            (trees[2], [0, 1, 3]),
            (trees[3], [6, 5, 3]),
            (trees[4], [0, 1, 4, 5, 3]),
            (trees[5], [2, 1, 6, 5, 3]),
            (trees[6], [0, 2, 1, 4, 6, 5, 3]),
        )
        for tree, res in items:
            assert list(n.key for n in BTUtil.postorder(tree)) == res

    def test_levelorder(self, trees: List[BTNode]):
        items = (
            (trees[0], []),
            (trees[1], [3]),
            (trees[2], [3, 1, 0]),
            (trees[3], [3, 5, 6]),
            (trees[4], [3, 1, 5, 0, 4]),
            (trees[5], [3, 1, 5, 2, 6]),
            (trees[6], [3, 1, 5, 0, 2, 4, 6]),
        )
        for tree, res in items:
            assert list(n.key for level in BTUtil.levelorder(tree) for n in level) == res

    def test_levelorder_with_none(self, trees: List[BTNode]):
        items = (
            (trees[0], []),
            (trees[1], [3, None, None]),
            (trees[2], [3, 1, None, 0, None, None, None]),
            (trees[3], [3, None, 5, None, 6, None, None]),
            (trees[4], [3, 1, 5, 0, None, 4, None, None, None, None, None]),
            (trees[5], [3, 1, 5, None, 2, None, 6, None, None, None, None]),
            (trees[6], [3, 1, 5, 0, 2, 4, 6] + [None] * 8),
        )
        for tree, res in items:
            assert list(n and n.key for level in BTUtil.levelorder(tree, filter_none=False) for n in level) == res

    def test_is_equal(self):
        f = BTUtil.is_equal
        gen = BTUtil.gen_tree
        # 空树是相等的
        assert f(gen([]), gen([]))
        # 第一个树 5 是 2 的右节点, 第二个则是左节点
        assert not f(gen([1, 2, 3, None, 5]), gen([1, 2, 3, 5]))
        assert f(gen([1, 2, 3, None, 5]), gen([1, 2, 3, None, 5]))
