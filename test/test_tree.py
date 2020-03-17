import pytest

from structure import BinaryTreeNode, BinaryTree, BinaryTreeRecursion


@pytest.fixture
def trees():
    """返回如下的五棵树 (最大层数: 3).
    ```
        1         1      N      1        1
      2   3     2   N         N   9    2   3
     N 5 N N   9 N               8 N
    ```
    """
    return [
        BinaryTreeNode.from_list([1, 2, 3, None, 5]),
        BinaryTreeNode.from_list([1, 2, None, 9, None]),
        BinaryTreeNode.from_list([None]),
        BinaryTreeNode.from_list([1, None, 9, None, None, 8, None]),
        BinaryTreeNode.from_list([1, 2, 3]),
    ]


def test_preorder(trees):
    fs = [BinaryTree.preorder, BinaryTree._preorder,
          BinaryTreeRecursion.preorder]
    for f in fs:
        assert list(n.val for n in f(trees[0])) == [1, 2, 5, 3]
        assert list(n.val for n in f(trees[1])) == [1, 2, 9]
        assert list(n.val for n in f(trees[2])) == []
        assert list(n.val for n in f(trees[3])) == [1, 9, 8]
        assert list(n.val for n in f(trees[4])) == [1, 2, 3]


def test_inorder(trees):
    fs = [BinaryTree.inorder]
    for f in fs:
        assert list(n.val for n in f(trees[0])) == [2, 5, 1, 3]
        assert list(n.val for n in f(trees[1])) == [9, 2, 1]
        assert list(n.val for n in f(trees[2])) == []
        assert list(n.val for n in f(trees[3])) == [1, 8, 9]
        assert list(n.val for n in f(trees[4])) == [2, 1, 3]
