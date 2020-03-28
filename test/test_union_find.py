from itertools import combinations

from structure.union_find import UnionFindV1


def test_union_find():
    uf = UnionFindV1.generate(10)

    # 逐步将 0, 1, 2, 9 四个元素放到一个集合中.
    assert uf._ids == list(range(10))
    assert not uf.is_connected(0, 9)
    uf.union(0, 9)
    assert uf._ids == [9, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert uf.is_connected(0, 9)
    uf.union(1, 2)
    assert uf.is_connected(1, 2)
    assert uf._ids == [9, 2, 2, 3, 4, 5, 6, 7, 8, 9]
    uf.union(0, 1)
    for p, q in combinations((0, 1, 2, 9), r=2):
        assert uf.is_connected(p, q)
    assert uf._ids == [2, 2, 2, 3, 4, 5, 6, 7, 8, 2]
