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


@pytest.mark.parametrize('f', (BinaryTree.preorder,
                               BinaryTree._preorder,
                               BinaryTreeRecursion.preorder))
def test_preorder(trees, f):
    assert list(n.val for n in f(trees[0])) == [1, 2, 5, 3]
    assert list(n.val for n in f(trees[1])) == [1, 2, 9]
    assert list(n.val for n in f(trees[2])) == []
    assert list(n.val for n in f(trees[3])) == [1, 9, 8]
    assert list(n.val for n in f(trees[4])) == [1, 2, 3]


@pytest.mark.parametrize('f', (BinaryTree.inorder,))
def test_inorder(trees, f):
    assert list(n.val for n in f(trees[0])) == [2, 5, 1, 3]
    assert list(n.val for n in f(trees[1])) == [9, 2, 1]
    assert list(n.val for n in f(trees[2])) == []
    assert list(n.val for n in f(trees[3])) == [1, 8, 9]
    assert list(n.val for n in f(trees[4])) == [2, 1, 3]


@pytest.mark.parametrize('f', (BinaryTree.postorder,))
def test_postorder(trees, f):
    assert list(n.val for n in f(trees[0])) == [5, 2, 3, 1]
    assert list(n.val for n in f(trees[1])) == [9, 2, 1]
    assert list(n.val for n in f(trees[2])) == []
    assert list(n.val for n in f(trees[3])) == [8, 9, 1]
    assert list(n.val for n in f(trees[4])) == [2, 3, 1]


@pytest.mark.parametrize('f', (BinaryTree.levelorder,))
def test_levelorder(trees, f):
    assert list(n.val for level in f(trees[0]) for n in level) == [1, 2, 3, 5]
    assert list(n.val for level in f(trees[1]) for n in level) == [1, 2, 9]
    assert list(n.val for level in f(trees[2]) for n in level) == []
    assert list(n.val for level in f(trees[3]) for n in level) == [1, 9, 8]
    assert list(n.val for level in f(trees[4]) for n in level) == [1, 2, 3]
