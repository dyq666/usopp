from itertools import count

import pytest

from structure import HashTable
from structure.hashtable import StudentV1, StudentV2


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
        ht = MockHashTable()
        counter = count()

        assert len(ht) == 0
        assert ht._capacity == HashTable.CAPACITYS[0]

        # 扩容测试
        for i in range(len(HashTable.CAPACITYS)):
            for _ in range(HashTable.CAPACITYS[i] * 3 + 1):
                num = next(counter)
                ht[num] = str(num)
            # 到最大容量了, 不能继续扩容了.
            if i == len(HashTable.CAPACITYS) - 1:
                assert ht._capacity == HashTable.CAPACITYS[i]
            else:
                assert ht._capacity == HashTable.CAPACITYS[i + 1]

        # TODO 缩容测试


def test_student():
    studentv1_a1 = StudentV1(1, 2, 'aaa')
    studentv1_a2 = StudentV1(1, 2, 'aaa')
    assert studentv1_a1 != studentv1_a2
    assert studentv1_a1 is not studentv1_a2
    assert len({studentv1_a1, studentv1_a2}) == 2

    studentv2_a1 = StudentV2(1, 2, 'aaa')
    studentv2_a2 = StudentV2(1, 2, 'aaa')
    assert studentv2_a1 == studentv2_a2
    assert studentv2_a1 is not studentv2_a2
    assert len({studentv2_a1, studentv2_a2}) == 1
