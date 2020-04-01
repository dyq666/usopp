from structure import AVL, BST


def test_add():
    """
    一些简单树的四种情况, LL, LR, RR, RL.
    ```
      3       2      3        2     1            2     1         2
     2   ->  1 3    1    ->  1 3      2     ->  1 3     3  ->   1 3
    1                2                  3              2
    ```
    """
    items = (
        ([3, 2, 1], [2, 1, 3]),
        ([3, 1, 2], [2, 1, 3]),
        ([1, 2, 3], [2, 1, 3]),
        ([1, 3, 2], [2, 1, 3]),
    )
    for array, res in items:
        avl = AVL.from_iterable(array)
        assert len(avl) == len(array)
        assert list(avl) == res
        assert BST.is_bst(avl._root)
        assert AVL.is_avl(avl._root)
