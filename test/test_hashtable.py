import pytest

from structure import HashTable


class MockHashTable(HashTable):
    UPPER = 3  # 改成一个更小的值, 方便测试


class TestHashTable:

    def test_basic(self):
        ht = MockHashTable()
        test_size = int(HashTable.CAPACITYS[0] * 3.11)

        for i in range(test_size):
            ht[i] = str(i)
            assert len(ht) == i + 1
            assert set(ht) == {(j, str(j)) for j in range(i + 1)}
            assert i in ht
            assert ht[i] == str(i)
        # 增加元素期间扩容一次
        assert ht._capacity == HashTable.CAPACITYS[1]

        for i in range(test_size):
            del ht[i]
            assert len(ht) == test_size - (i + 1)
            assert set(ht) == {(j, str(j)) for j in range(i + 1, test_size)}
            assert i not in ht
            with pytest.raises(KeyError):
                assert ht[i] == str(i)
        # 删除元素期间缩容一次
        assert ht._capacity == HashTable.CAPACITYS[0]

    def test_resize(self):
        # TODO finish it
        pass
