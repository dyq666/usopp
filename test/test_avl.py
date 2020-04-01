from structure import AVL, BST


def test_add():
    """
    一些简单树的四种情况, LL, LR, RR, RL.
    ```
      3       2      3        2     1            2     1         2
     2   ->  1 3    1    ->  1 3      2     ->  1 3     3  ->   1 3
    1                2                  3              2
    ```
    一些复杂树的四种情况, LL, LR, RR, RL (这里节点比较多, 就不写结果了).
    ```
          4         4         4         3
        1   5     1   5     0   6     0  6
      0  2      0  3           5 7      5 7
    -1空       空空2空         空空空8    4空空空
    ```
    """
    items = (
        ([3, 2, 1], [2, 1, 3]),
        ([3, 1, 2], [2, 1, 3]),
        ([1, 2, 3], [2, 1, 3]),
        ([1, 3, 2], [2, 1, 3]),
        ([4, 1, 5, 0, 2, -1], [1, 0, 4, -1, None, 2, 5]),
        ([4, 1, 5, 0, 3, 2], [3, 1, 4, 0, 2, None, 5]),
        ([4, 0, 6, 5, 7, 8], [6, 4, 7, 0, 5, None, 8]),
        ([3, 0, 6, 5, 7, 4], [5, 3, 6, 0, 4, None, 7]),
    )
    for array, res in items:
        avl = AVL.from_iterable(array)
        assert len(avl) == len(array)
        assert list(avl) == res
        assert BST.is_bst(avl._root)
        assert AVL.is_avl(avl._root)
