import pytest

from structure import BTNode, BT


@pytest.fixture
def trees():
    """返回如下的五棵树 (最大层数: 3).
    ```
        1         1      N      1        1       9
      2   3     2   N         N   9    2   3   8   7
     N 5       9 N               8 N          N 4 3 N
    ```
    """
    return [
        BTNode.from_list([1, 2, 3, None, 5]),
        BTNode.from_list([1, 2, None, 9, None]),
        BTNode.from_list([None]),
        BTNode.from_list([1, None, 9, None, None, 8, None]),
        BTNode.from_list([1, 2, 3]),
        BTNode.from_list([9, 8, 7, None, 4, 3, None])
    ]


@pytest.mark.parametrize('f', (BT.preorder,
                               BT.preorder_with_mocked_stack,
                               BT.preorder_with_recursion,))
def test_preorder(trees, f):
    assert list(n.val for n in f(trees[0])) == [1, 2, 5, 3]
    assert list(n.val for n in f(trees[1])) == [1, 2, 9]
    assert list(n.val for n in f(trees[2])) == []
    assert list(n.val for n in f(trees[3])) == [1, 9, 8]
    assert list(n.val for n in f(trees[4])) == [1, 2, 3]


@pytest.mark.parametrize('f', (BT.inorder,))
def test_inorder(trees, f):
    assert list(n.val for n in f(trees[0])) == [2, 5, 1, 3]
    assert list(n.val for n in f(trees[1])) == [9, 2, 1]
    assert list(n.val for n in f(trees[2])) == []
    assert list(n.val for n in f(trees[3])) == [1, 8, 9]
    assert list(n.val for n in f(trees[4])) == [2, 1, 3]


@pytest.mark.parametrize('f', (BT.postorder,))
def test_postorder(trees, f):
    assert list(n.val for n in f(trees[0])) == [5, 2, 3, 1]
    assert list(n.val for n in f(trees[1])) == [9, 2, 1]
    assert list(n.val for n in f(trees[2])) == []
    assert list(n.val for n in f(trees[3])) == [8, 9, 1]
    assert list(n.val for n in f(trees[4])) == [2, 3, 1]


@pytest.mark.parametrize('f', (BT.levelorder,))
def test_levelorder(trees, f):
    assert list(n.val for level in f(trees[0]) for n in level) == [1, 2, 3, 5]
    assert list(n.val for level in f(trees[1]) for n in level) == [1, 2, 9]
    assert list(n.val for level in f(trees[2]) for n in level) == []
    assert list(n.val for level in f(trees[3]) for n in level) == [1, 9, 8]
    assert list(n.val for level in f(trees[4]) for n in level) == [1, 2, 3]
    assert list(n.val for level in f(trees[5]) for n in level) == [9, 8, 7, 4, 3]

    assert list(n and n.val for level in f(trees[0], False) for n in level) == [1, 2, 3, None, 5]
    assert list(n and n.val for level in f(trees[1], False) for n in level) == [1, 2, None, 9, None]
    assert list(n and n.val for level in f(trees[2], False) for n in level) == []
    assert list(n and n.val for level in f(trees[3], False) for n in level) == [1, None, 9, 8, None]
    assert list(n and n.val for level in f(trees[4], False) for n in level) == [1, 2, 3]
    assert list(n and n.val for level in f(trees[5], False) for n in level) == [9, 8, 7, None, 4, 3, None]
