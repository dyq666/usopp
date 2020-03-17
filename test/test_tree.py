import pytest

from structure import BinaryTreeNode, BinaryTree


@pytest.fixture
def trees():
    """返回如下的五棵树.
    ```
        1         1      N      1        1
      2   3     2   N         N   9    2   3
     N 5 N N   9 N N N       N N 8 N
    ```
    """
    return [
        BinaryTreeNode.from_list([1, 2, 3, None, 5, None, None]),
        BinaryTreeNode.from_list([1, 2, None, 9, None, None, None]),
        BinaryTreeNode.from_list([None]),
        BinaryTreeNode.from_list([1, None, 9, None, None, 8, None]),
        BinaryTreeNode.from_list([1, 2, 3]),
    ]


def test_inorder(trees):

    fs = [BinaryTree.inorder, BinaryTree._inorder]

    for f in fs:
        assert list(n.val for n in f(trees[0])) == [2, 5, 1, 3]
        assert list(n.val for n in f(trees[1])) == [9, 2, 1]
        assert list(n.val for n in f(trees[2])) == []
        assert list(n.val for n in f(trees[3])) == [1, 8, 9]
        assert list(n.val for n in f(trees[4])) == [2, 1, 3]
