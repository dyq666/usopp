from structure import HashTable


def test_hashtable():
    ht = HashTable()

    for i in range(ht._m * 2):
        ht.add(i, str(i))
        assert len(ht) == i + 1
        assert set(ht) == set(range(i + 1))
