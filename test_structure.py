import pytest

from structure import DynamicArray


class TestDynamicArray:

    def test_normal(self):
        d = DynamicArray()
        # 默认情况下容量是 10, 大小是 0
        assert len(d._data) == d.MIN_SIZE
        assert len(d) == 0

    def test_insert(self):
        d = DynamicArray()

        # 不能在小于 0 或大于 size 的位置插入元素
        with pytest.raises(IndexError):
            d.insert('a', -1)
        with pytest.raises(IndexError):
            d.insert('a', len(d) + 1)

        # 从末尾插入 10 个元素
        for i in range(1, 11):
            d.insert('c')
            assert len(d._data) == 10
            assert len(d) == i
        # 插入结束后 size == capactiy
        assert len(d) == len(d._data)

        # 再插入 10 个元素, 此时容量变成之前的两倍
        for i in range(11, 21):
            d.insert('zzz')
            assert len(d._data) == 20
            assert len(d) == i

    def test_pop(self):
        d = DynamicArray()
        for i in range(20):
            d.insert(i)

        # 不能在小于 0 或大于 size - 1 的位置茶元素
        with pytest.raises(IndexError):
            d.pop(-1)
        with pytest.raises(IndexError):
            d.pop(len(d))

        # 从末尾删除元素
        for i in range(14):
            assert 19 - i == d.pop()
            assert len(d._data) == 20
            assert len(d) == 19 - i

        # 缩容, 20 // 4 == 5
        assert len(d) == 6
        assert len(d._data) == 20
        d.pop()
        assert len(d) == 5
        assert len(d._data) == 10

        # 由于限制了容量必须 >= 10, 所以当 10 // 4 = 2 时, 也没有缩容.
        for i in range(5):
            d.pop()
            assert len(d) == 4 - i
            assert len(d._data) == 10

        # 空数组不能 pop
        with pytest.raises(IndexError):
            d.pop()

    def test_contains(self):
        d = DynamicArray()
        for i in range(9):
            d.insert(i)

        # None 在底层的静态数组中, 但不在动态数组中
        assert None not in d
        assert None in d._data

        for i in range(9):
            assert i in d

    def test_iter(self):
        d = DynamicArray()

        # 空数组
        assert list(iter(d)) == []

        # 插满元素
        for i in range(d.MIN_SIZE):
            d.insert(i)
        assert list(iter(d)) == list(range(d.MIN_SIZE))

        # 扩容
        d.insert(100, 1)
        assert list(iter(d)) == [0, 100, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert d._data == [0, 100, 1, 2, 3, 4, 5, 6, 7, 8,
                           9, None, None, None, None, None, None, None, None, None]

        # 删除
        d.pop(2)
        assert list(iter(d)) == [0, 100, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_get_and_set(self):
        d = DynamicArray()
        for i in range(d.MIN_SIZE):
            d.insert(i)

        # 不能在小于 0 或大于 size 的位置 get / set 元素
        with pytest.raises(IndexError):
            temp = d[-1]
        with pytest.raises(IndexError):
            temp = d[len(d)]
        with pytest.raises(IndexError):
            d[-1] = 1
        with pytest.raises(IndexError):
            d[len(d)] = 1

        for i in range(d.MIN_SIZE):
            assert d[i] == i
        for i in range(d.MIN_SIZE):
            d[i] = i * 100
        for i in range(d.MIN_SIZE):
            assert d[i] == i * 100
