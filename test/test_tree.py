import operator
from functools import partial
from typing import List, Optional

import pytest

from structure import (
    BST, BTNode, BTUtil, SegmentTree, SegmentTreeWithNode,
    Trie,
)


@pytest.fixture
def trees(bst_arrays: List[List[Optional[int]]]) -> List[BTNode]:
    """返回一些树 (最大层数: 3)."""
    return [BTNode.from_iterable(a) for a in bst_arrays]


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


@pytest.fixture
def segement_arrays() -> List[List[int]]:
    """空, 奇数个, 偶数个."""
    return [
        [],
        [1, 4, 8],
        [1, 2, 5, 9],
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

    def test_get_and_contains(self, bst_arrays: List[List[Optional[int]]]):
        tree = BST.from_iteralbe(bst_arrays[6])
        assert tree.get(7) is None
        assert tree.get(6).val == 6
        assert tree.get(7, 100) == 100

        assert 7 not in tree
        assert 6 in tree


class TestBTUtil:

    @pytest.mark.parametrize('f', (BTUtil.preorder,
                                   BTUtil.preorder_with_mocked_stack,
                                   BTUtil.preorder_with_recursion,))
    def test_preorder(self, f: callable, trees: List[BTNode]):
        assert list(n.val for n in f(trees[0])) == []
        assert list(n.val for n in f(trees[1])) == [3]
        assert list(n.val for n in f(trees[2])) == [3, 1, 0]
        assert list(n.val for n in f(trees[3])) == [3, 5, 6]
        assert list(n.val for n in f(trees[4])) == [3, 1, 0, 5, 4]
        assert list(n.val for n in f(trees[5])) == [3, 1, 2, 5, 6]
        assert list(n.val for n in f(trees[6])) == [3, 1, 0, 2, 5, 4, 6]

    @pytest.mark.parametrize('f', (partial(BTUtil.preorder, skip_none=False),
                                   BTUtil.preorder_with_mocked_stack_and_none,
                                   BTUtil.preorder_with_recursion_and_none,))
    def test_preorder_with_none(self, f: callable, trees: List[BTNode]):
        assert list(n and n.val for n in f(trees[0])) == []
        assert list(n and n.val for n in f(trees[1])) == [3]
        assert list(n and n.val for n in f(trees[2])) == [3, 1, 0, None, None]
        assert list(n and n.val for n in f(trees[3])) == [3, None, 5, None, 6]
        assert list(n and n.val for n in f(trees[4])) == [3, 1, 0, None, 5, 4, None]
        assert list(n and n.val for n in f(trees[5])) == [3, 1, None, 2, 5, None, 6]
        assert list(n and n.val for n in f(trees[6])) == [3, 1, 0, 2, 5, 4, 6]

    @pytest.mark.parametrize('f', (BTUtil.inorder,))
    def test_inorder(self, f: callable, trees: List[BTNode]):
        assert list(n and n.val for n in f(trees[0])) == []
        assert list(n and n.val for n in f(trees[1])) == [3]
        assert list(n and n.val for n in f(trees[2])) == [0, 1, 3]
        assert list(n and n.val for n in f(trees[3])) == [3, 5, 6]
        assert list(n and n.val for n in f(trees[4])) == [0, 1, 3, 4, 5]
        assert list(n and n.val for n in f(trees[5])) == [1, 2, 3, 5, 6]
        assert list(n and n.val for n in f(trees[6])) == [0, 1, 2, 3, 4, 5, 6]

    @pytest.mark.parametrize('f', (BTUtil.postorder,))
    def test_postorder(self, f: callable, trees: List[BTNode]):
        assert list(n and n.val for n in f(trees[0])) == []
        assert list(n and n.val for n in f(trees[1])) == [3]
        assert list(n and n.val for n in f(trees[2])) == [0, 1, 3]
        assert list(n and n.val for n in f(trees[3])) == [6, 5, 3]
        assert list(n and n.val for n in f(trees[4])) == [0, 1, 4, 5 , 3]
        assert list(n and n.val for n in f(trees[5])) == [2, 1, 6, 5, 3]
        assert list(n and n.val for n in f(trees[6])) == [0, 2, 1, 4, 6, 5, 3]

    @pytest.mark.parametrize('f', (BTUtil.levelorder,))
    def test_levelorder(self, f: callable, trees: List[BTNode]):
        assert list(n.val for level in f(trees[0]) for n in level) == []
        assert list(n.val for level in f(trees[1]) for n in level) == [3]
        assert list(n.val for level in f(trees[2]) for n in level) == [3, 1, 0]
        assert list(n.val for level in f(trees[3]) for n in level) == [3, 5, 6]
        assert list(n.val for level in f(trees[4]) for n in level) == [3, 1, 5, 0, 4]
        assert list(n.val for level in f(trees[5]) for n in level) == [3, 1, 5, 2, 6]
        assert list(n.val for level in f(trees[6]) for n in level) == [3, 1, 5, 0, 2, 4, 6]

    @pytest.mark.parametrize('f', (partial(BTUtil.levelorder, skip_none=False),))
    def test_levelorder_with_none(self, f: callable, trees: List[BTNode]):
        assert list(n and n.val for level in f(trees[0]) for n in level) == []
        assert list(n and n.val for level in f(trees[1]) for n in level) == [3]
        assert list(n and n.val for level in f(trees[2]) for n in level) == [3, 1, None, 0, None]
        assert list(n and n.val for level in f(trees[3]) for n in level) == [3, None, 5, None, 6]
        assert list(n and n.val for level in f(trees[4]) for n in level) == [3, 1, 5, 0, None, 4, None]
        assert list(n and n.val for level in f(trees[5]) for n in level) == [3, 1, 5, None, 2, None, 6]
        assert list(n and n.val for level in f(trees[6]) for n in level) == [3, 1, 5, 0, 2, 4, 6]

    def test_is_equal(self):
        f = BTUtil.is_equal
        gen = BTNode.from_iterable
        assert f(gen([]), gen([]))
        # 第一个树 5 是 2 的右节点, 第二个则是左节点
        assert not f(gen([1, 2, 3, None, 5]), gen([1, 2, 3, 5]))
        assert f(gen([1, 2, 3, None, 5]), gen([1, 2, 3, None, 5]))


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


def test_trie():
    """测试以下字典树:
    ```
    N   N          N              N
       a       d   a   e      d   a   e
              d f     c f    d *f*  *c* f
                 g   h          g   h
    ```

      - 空
      - 只有一个字符
      - 所有字符串都是到叶子节点才终止
      - 部分字符串到非叶子节点终止 (用 ** 标记)
    """
    words_set = (
        set(),
        {'a'},
        {'dd', 'dfg', 'a', 'ech', 'ef'},
        {'dd', 'df', 'dfg', 'a', 'ec', 'ech', 'ef'},
    )

    for words in words_set:
        trie = Trie.from_iterable(words)
        assert set(trie) == words

        for word in words:
            for i in range(1, len(word) + 1):
                # 字符串的子串如果不是一个单词, 那么就不应该在 `trie` 中.
                if i < len(word) and word[:i] not in words:
                    assert word[:i] not in trie
                else:
                    assert word[:i] in trie
