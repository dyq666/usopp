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


def test_remove():
    """
    一些简单树的四种情况, ** 代表删除的元素, LL, LR, RR, RL.
    ```
      3        3         3         3
     2 *4*    1 *4*   *1*  4     *1* 5
    1          2             5      4

    一些复杂树的四种情况, ** 代表删除的元素, LL, LR, RR, RL.
    ```
          4            4            4           3
        1   5        1   5        2   6       2  6
      0  2   *6*   0  3   *6*   *1*  5 7    *1* 5 7
    -1空          空空2空            空空空8      4空空空
    ```

    TODO 一些删除侧复杂的情况, 主要是测试 `AVL._pop_max_from` 中的 balance.
    """
    items = (
        ([3, 2, 4, 1], 4, [2, 1, 3]),
        ([3, 1, 4, 2], 4, [2, 1, 3]),
        ([3, 1, 4, 5], 1, [4, 3, 5]),
        ([3, 1, 5, 4], 1, [4, 3, 5]),
        ([4, 1, 5, 0, 2, 6, -1], 6, [1, 0, 4, -1, None, 2, 5]),
        ([4, 1, 5, 0, 3, 6, 2], 6, [3, 1, 4, 0, 2, None, 5]),
        ([4, 2, 6, 1, 5, 7, 8], 1, [6, 4, 7, 2, 5, None, 8]),
        ([3, 2, 6, 1, 5, 7, 4], 1, [5, 3, 6, 2, 4, None, 7]),
    )
    for array, delete, res in items:
        avl = AVL.from_iterable(array)
        avl.remove(delete)
        assert list(avl) == res
        assert BST.is_bst(avl._root)
        assert AVL.is_avl(avl._root)
