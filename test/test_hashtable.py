from itertools import count

import pytest

from structure import HashTable


class MockHashTable(HashTable):
    UPPER = 3  # 改成一个更小的值, 方便测试


class TestHashTable:

    def test_basic(self):
        ht = MockHashTable()
        # 乘以 1.1 的目的是保证增加和删除期间分别修改一次容量
        test_size = int(ht.CAPACITYS[0] * ht.UPPER * 1.1)

        # 测试添加元素
        for i in range(test_size):
            k, v = i, str(i)
            ht.add(k, v)
            assert len(ht) == i + 1
            assert set(ht) == {(j, str(j)) for j in range(i + 1)}
            assert k in ht
            assert ht.get(k) == v
        # 增加元素期间扩容一次
        assert ht._capacity == ht.CAPACITYS[1]

        # 测试删除元素
        for i in range(test_size):
            k, v = i, str(i)
            ht.remove(k)
            assert len(ht) == test_size - (i + 1)
            assert set(ht) == {(j, str(j)) for j in range(i + 1, test_size)}
            assert k not in ht
            with pytest.raises(KeyError):
                ht.get(k)
            with pytest.raises(KeyError):
                ht.remove(k)
        # 删除元素期间缩容一次
        assert ht._capacity == ht.CAPACITYS[0]

        # 测试更新元素
        ht.add(2, 3)
        ht.add('2', 3)
        assert ht.get(2) == 3
        assert ht.get('2') == 3
        ht.add(2, 4)
        assert ht.get(2) == 4
        assert ht.get('2') == 3

    def test_resize(self):
        ht = MockHashTable()

        # 初始容量
        assert len(ht) == 0
        assert ht._capacity == ht.CAPACITYS[0]

        # 测试容量是否正确扩展.
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

        # 测试容量是否正确缩小.
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
