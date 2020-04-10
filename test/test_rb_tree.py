from structure import Tree23


def test_tree23():
    # 测试向根节点插入 1 个元素
    tree23 = Tree23.from_iterable([1])
    assert list(tree23) == [[1]]
    assert len(tree23) == 1

    # 测试向根节点插入 2 个元素
    tree23 = Tree23.from_iterable([2, 1])
    assert list(tree23) == [[1, 2]]
    assert len(tree23) == 2
    tree23 = Tree23.from_iterable([1, 2])
    assert list(tree23) == [[1, 2]]
    assert len(tree23) == 2
    tree23 = Tree23.from_iterable([1])
    assert list(tree23) == [[1]]
    assert len(tree23) == 1
