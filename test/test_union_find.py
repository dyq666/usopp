from itertools import combinations

import pytest

from structure.union_find import UnionFindV1, UnionFindV2


@pytest.mark.parametrize('f', (UnionFindV1.generate,
                               UnionFindV2.generate,))
def test_union_find(f: callable):
    uf = f(10)

    # 逐步将 0, 1, 2, 9 四个元素放到一个集合中.
    assert not uf.is_connected(0, 9)
    uf.union(0, 9)
    assert uf.is_connected(0, 9)
    uf.union(1, 2)
    assert uf.is_connected(1, 2)
    uf.union(0, 1)
    for p, q in combinations((0, 1, 2, 9), r=2):
        assert uf.is_connected(p, q)
