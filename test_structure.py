import pytest

from structure import DynamicArrayV1, DynamicArrayV2, LoopArray


@pytest.mark.parametrize('cls', (DynamicArrayV1, DynamicArrayV2))
def test_DynamicArrayV1_and_part_of_DynamicArrayV2(cls):
    """测试 `DynamicArrayV1` 的所有方法, 以及 `DynamicArrayV2` 中和栈相关的方法.

    1. 检查初始状态的静态数组和动态数组, 初始状态不能 `pop`.
    2. `append` 2 个元素, 查看静态数组和动态数组, 再 `pop` 2 个元素,
       观察元素是否和 `append` 顺序相反, 查看静态数组和动态数组, 此时不能 `pop`.
    3. `append` 10 个元素, 查看静态数组和动态数组, 再 `append` 1 个元素, 查看是否扩容.
    4. `pop` 5 个元素, 查看静态数组和动态数组, 再 `pop` 1 个元素, 查看是否缩容.
    """
    array = cls()

    # 1
    assert array._data == [None for _ in range(10)]
    assert list(array) == []
    with pytest.raises(IndexError):
        array.pop()

    # 2
    for i in range(2):
        array.append(i)
    assert array._data == list(range(2)) + [None for _ in range(8)]
    assert list(array) == [0, 1]
    for i in range(1, -1, -1):
        assert i == array.pop()
    assert array._data == [None for _ in range(10)]
    assert list(array) == []
    with pytest.raises(IndexError):
        array.pop()

    # 3
    for i in range(10):
        array.append(i)
    assert array._data == list(array) == list(range(10))
    array.append(10)
    assert array._data == list(range(11)) + [None for _ in range(9)]
    assert list(array) == list(range(11))

    # 4
    for _ in range(5):
        array.pop()
    assert array._data == list(range(6)) + [None for _ in range(14)]
    assert list(array) == list(range(6))
    array.pop()
    assert array._data == list(range(5)) + [None for _ in range(5)]
    assert list(array) == list(range(5))


class TestDynamicArrayV2:

    def test_normal(self):
        d = DynamicArrayV2()
        # 默认情况下容量是 10, 大小是 0
        assert len(d._data) == d.MIN_SIZE
        assert len(d) == 0

    def test_insert(self):
        d = DynamicArrayV2()

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
        d = DynamicArrayV2()
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
        d = DynamicArrayV2()
        for i in range(9):
            d.insert(i)

        # None 在底层的静态数组中, 但不在动态数组中
        assert None not in d
        assert None in d._data

        for i in range(9):
            assert i in d

    def test_iter(self):
        d = DynamicArrayV2()

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
        assert d._data == [0, 100, 2, 3, 4, 5, 6, 7, 8, 9,
                           None, None, None, None, None, None, None, None, None, None]

    def test_get_and_set(self):
        d = DynamicArrayV2()
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


def test_LoopArray():
    """
    1. 查看初始状态的静态数组和动态数组, 初始状态不能 `popleft`.
    2. `append` 2 个元素, 查看静态数组和动态数组, 再 `popleft` 2 个元素,
       观察元素是否和 `append` 相同, 查看静态数组和动态数组, 此时不能 `popleft`.
    3. `append` 8 个元素,  `popleft` 6 个元素, 查看静态数组和动态数组.
    4. `append` 1 个元素, 查看静态数组和动态数组是否正确的扩容.
    5. `popleft` 1 个元素, 查看静态数组和动态数组是否正确的缩容.
    """
    array = LoopArray()

    # 1
    assert array._data == [None for _ in range(10)]
    assert list(array) == []
    assert None not in array
    with pytest.raises(IndexError):
        array.popleft()

    # 2
    for i in range(2):
        array.append(i)
        assert i in array
    assert array._data == list(range(2)) + [None for _ in range(8)]
    assert list(array) == [0, 1]
    for i in range(2):
        assert i == array.popleft()
        assert i not in array
    assert array._data == [None for _ in range(10)]
    assert list(array) == []

    # 3
    for i in range(8):
        array.append(i)
    for i in range(6):
        assert i == array.popleft()
    assert array._data == [None for _ in range(8)] + list(range(6, 8))
    assert list(array) == [6, 7]

    # 4
    array.append('c')
    assert array._data == [6, 7, 'c'] + [None for _ in range(17)]
    assert list(array) == [6, 7, 'c']

    # 5
    assert 6 == array.popleft()
    assert array._data == [7, 'c'] + [None for _ in range(8)]
    assert list(array) == [7, 'c']
