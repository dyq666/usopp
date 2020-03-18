from functools import partial

import pytest

from structure import BTNode, BTUtil
from util import no_value


@pytest.fixture
def trees():
    """返回如下的一些树 (最大层数: 3).
    ```
        1         1      N      1        1       9
      2   3     2   N         N   9    2   3   8   7
     N 5       9 N               8 N          N 4 3 N
    ```
    """
    return [
        BTNode.from_iterable([1, 2, 3, no_value, 5]),
        BTNode.from_iterable([1, 2, no_value, 9, no_value]),
        BTNode.from_iterable([no_value]),
        BTNode.from_iterable([1, no_value, 9, no_value, no_value, 8, no_value]),
        BTNode.from_iterable([1, 2, 3]),
        BTNode.from_iterable([9, 8, 7, no_value, 4, 3, no_value])
    ]


@pytest.mark.parametrize('f', (BTUtil.preorder,
                               BTUtil.preorder_with_mocked_stack,
                               BTUtil.preorder_with_recursion,))
def test_preorder(trees, f):
    assert list(n.val for n in f(trees[0])) == [1, 2, 5, 3]
    assert list(n.val for n in f(trees[1])) == [1, 2, 9]
    assert list(n.val for n in f(trees[2])) == []
    assert list(n.val for n in f(trees[3])) == [1, 9, 8]
    assert list(n.val for n in f(trees[4])) == [1, 2, 3]
    assert list(n.val for n in f(trees[5])) == [9, 8, 4, 7, 3]


@pytest.mark.parametrize('f', (partial(BTUtil.preorder, skip_none=False),
                               BTUtil.preorder_with_mocked_stack_and_none,
                               BTUtil.preorder_with_recursion_and_none))
def test_preorder_with_none(trees, f):
    assert list(n and n.val for n in f(trees[0])) == [1, 2, None, 5, 3]
    assert list(n and n.val for n in f(trees[1])) == [1, 2, 9, None, None]
    assert list(n and n.val for n in f(trees[2])) == []
    assert list(n and n.val for n in f(trees[3])) == [1, None, 9, 8, None]
    assert list(n and n.val for n in f(trees[4])) == [1, 2, 3]
    assert list(n and n.val for n in f(trees[5])) == [9, 8, None, 4, 7, 3, None]


@pytest.mark.parametrize('f', (BTUtil.inorder,))
def test_inorder(trees, f):
    assert list(n.val for n in f(trees[0])) == [2, 5, 1, 3]
    assert list(n.val for n in f(trees[1])) == [9, 2, 1]
    assert list(n.val for n in f(trees[2])) == []
    assert list(n.val for n in f(trees[3])) == [1, 8, 9]
    assert list(n.val for n in f(trees[4])) == [2, 1, 3]
    assert list(n.val for n in f(trees[5])) == [8, 4, 9, 3, 7]


@pytest.mark.parametrize('f', (BTUtil.postorder,))
def test_postorder(trees, f):
    assert list(n.val for n in f(trees[0])) == [5, 2, 3, 1]
    assert list(n.val for n in f(trees[1])) == [9, 2, 1]
    assert list(n.val for n in f(trees[2])) == []
    assert list(n.val for n in f(trees[3])) == [8, 9, 1]
    assert list(n.val for n in f(trees[4])) == [2, 3, 1]
    assert list(n.val for n in f(trees[5])) == [4, 8, 3, 7, 9]


@pytest.mark.parametrize('f', (BTUtil.levelorder,))
def test_levelorder(trees, f):
    assert list(n.val for level in f(trees[0]) for n in level) == [1, 2, 3, 5]
    assert list(n.val for level in f(trees[1]) for n in level) == [1, 2, 9]
    assert list(n.val for level in f(trees[2]) for n in level) == []
    assert list(n.val for level in f(trees[3]) for n in level) == [1, 9, 8]
    assert list(n.val for level in f(trees[4]) for n in level) == [1, 2, 3]
    assert list(n.val for level in f(trees[5]) for n in level) == [9, 8, 7, 4, 3]


@pytest.mark.parametrize('f', (partial(BTUtil.levelorder, skip_none=False),))
def test_levelorder(trees, f):
    assert list(n and n.val for level in f(trees[0]) for n in level) == [1, 2, 3, None, 5]
    assert list(n and n.val for level in f(trees[1]) for n in level) == [1, 2, None, 9, None]
    assert list(n and n.val for level in f(trees[2]) for n in level) == []
    assert list(n and n.val for level in f(trees[3]) for n in level) == [1, None, 9, 8, None]
    assert list(n and n.val for level in f(trees[4]) for n in level) == [1, 2, 3]
    assert list(n and n.val for level in f(trees[5]) for n in level) == [9, 8, 7, None, 4, 3, None]
