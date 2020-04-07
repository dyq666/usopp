import pytest

from structure import HashTable


def test_hashtable():
    ht = HashTable()

    for i in range(ht._m * 2):
        ht[i] = str(i)
        assert len(ht) == i + 1
        assert set(ht) == {(j, str(j)) for j in range(i + 1)}
        assert i in ht
        assert ht[i] == str(i)

    for i in range(ht._m * 2):
        del ht[i]
        assert len(ht) == ht._m * 2 - (i + 1)
        assert set(ht) == {(j, str(j)) for j in range(i + 1, ht._m * 2)}
        assert i not in ht
        with pytest.raises(KeyError):
            assert ht[i] == str(i)
