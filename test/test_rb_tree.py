from structure import Tree23


def test_tree23():
    tree23 = Tree23()
    tree23.add(1)
    assert list(tree23) == [[1]]
