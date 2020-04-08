from itertools import count

import pytest

from structure import HashTable
from structure.hashtable import StudentV1, StudentV2


class MockHashTable(HashTable):
    UPPER = 3  # 改成一个更小的值, 方便测试


class TestHashTable:

    def test_basic(self):
        ht = MockHashTable()
        test_size = int(ht.CAPACITYS[0] * 3.11)

        # 测试添加元素
        for i in range(test_size):
            ht.add(i, str(i))
            assert len(ht) == i + 1
            assert set(ht) == {(j, str(j)) for j in range(i + 1)}
            assert i in ht
            assert ht.get(i) == str(i)

        # 测试删除元素
        for i in range(test_size):
            ht.remove(i)
            assert len(ht) == test_size - (i + 1)
            assert set(ht) == {(j, str(j)) for j in range(i + 1, test_size)}
            assert i not in ht
            with pytest.raises(KeyError):
                assert ht.get(i) == str(i)
            with pytest.raises(KeyError):
                ht.remove(i)

        # 测试更新元素
        ht.add(2, 3)
        ht.add('2', 3)
        assert ht.get(2) == 3
        ht.add(2, 4)
        assert ht.get(2) == 4

    def test_resize(self):
        ht = MockHashTable()

        assert len(ht) == 0
        assert ht._capacity == ht.CAPACITYS[0]

        # 扩容测试
        asc_counter = count()
        for i in range(len(ht.CAPACITYS)):
            # len(self) = self._capacity * self.UPPER + 1 时就会扩容.
            for _ in range(ht._capacity * ht.UPPER + 1 - len(ht)):
                num = next(asc_counter)
                ht.add(num, str(num))
            # 到最大容量了, 不会继续扩容了.
            if i == len(ht.CAPACITYS) - 1:
                assert ht._capacity == ht.CAPACITYS[i]
            else:
                assert ht._capacity == ht.CAPACITYS[i + 1]

        # 缩容测试
        desc_counter = count(start=next(asc_counter) - 1, step=-1)
        for i in range(len(ht.CAPACITYS) - 1, -1, -1):
            # len(self) = self._capacity * self.LOWER - 1 时就会缩容.
            for _ in range(len(ht) - (ht._capacity * ht.LOWER - 1)):
                ht.remove(next(desc_counter))
            # 到最小容量了, 不会继续缩容了.
            if i == 0:
                assert ht._capacity == ht.CAPACITYS[i]
            else:
                assert ht._capacity == ht.CAPACITYS[i - 1]


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
