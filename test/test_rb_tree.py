from itertools import permutations

from structure import Tree23


def test_tree23():
    # 测试向根节点插入 1 个元素
    tree23 = Tree23.from_iterable([1])
    assert list(tree23) == [[1]]
    assert len(tree23) == 1

    # 测试向根节点插入 2 个元素
    for keys in permutations((1, 2)):
        tree23 = Tree23.from_iterable(keys)
        assert list(tree23) == [[1, 2]]
        assert len(tree23) == 2
    tree23 = Tree23.from_iterable([1, 1])
    assert list(tree23) == [[1]]
    assert len(tree23) == 1

    # 测试向根节点插入 3 个元素
    for keys in permutations((0, 1, 2)):
        tree23 = Tree23.from_iterable(keys)
        assert list(tree23) == [[1], [0], [2]]
        assert len(tree23) == 3
