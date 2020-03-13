import pytest

from structure import DynamicArrayV1, DynamicArrayV2, LoopArrayV1


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


def test_DynamicArrayV2():
    """测试 `DynamicArrayV2` 相较于 `DynamicArrayV1` 中新增的方法.

    1. 初始状态先插入 8 个元素, 随意选取一元素它应该在数组中, 而 `None` 不应该在.
    2. 从首尾分别插入元素, 分别查看插入后元素是否在数组中以及当前静态和动态数组.
    3. 从第 3 个位置插入元素, 此元素应该在数组中, 并查看是否扩容.
    4. 删除第 3 个位置元素, 此元素不应该再数组中, 从首删除两个元素, 从尾删除两个元素,
       查看此时容量, 在从首删除一个元素, 查看是否缩容.
    5. 测试从有效索引外 get 和 set, 应该报错. set 第四个索引的元素, 再获取此元素.
    """
    # 1
    array = DynamicArrayV2()
    for i in range(8):
        array.append(i)
    assert 5 in array
    assert None not in array

    # 2
    array.append(8)
    assert array._data == list(range(9)) + [None]
    assert list(array) == list(range(9))
    array.insert(0, -1)
    assert array._data == list(array) == list(range(-1, 9))

    # 3
    array.insert(2, 100)
    assert 100 in array
    assert array._data == list(range(-1, 1)) + [100] + list(range(1, 9)) + [None for _ in range(9)]
    assert list(array) == list(range(-1, 1)) + [100] + list(range(1, 9))

    # 4
    value = array.remove(2)
    assert value == 100 and value not in array
    for _ in range(2):
        array.pop()
    for _ in range(2):
        array.remove(0)
    assert array._capacity == 20
    assert len(array) == 6
    array.remove(0)
    assert array._capacity == 10
    assert len(array) == 5

    # 5, 此时数组为 [2, 3, 4, 5, 6]
    with pytest.raises(IndexError):
        array.remove(-1)
    with pytest.raises(IndexError):
        array.remove(len(array))
    with pytest.raises(IndexError):
        array.insert(-1, 200)
    with pytest.raises(IndexError):
        array.insert(len(array) + 1, 200)
    array[3] = 100
    assert array[3] == 100


def test_LoopArrayV1():
    """测试 `LoopArrayV1` 的所有方法

    1. 查看初始状态的静态数组和动态数组, 初始状态不能 `popleft`.
    2. `append` 2 个元素, 查看静态数组和动态数组, 再 `popleft` 2 个元素,
       观察元素是否和 `append` 相同, 查看静态数组和动态数组, 此时不能 `popleft`.
    3. `append` 8 个元素, `popleft` 6 个元素, 查看静态数组和动态数组.
    4. `append` 1 个元素, 查看静态数组和动态数组是否正确的扩容. (因为当前元素个数为 3, 2 * 3 < 10, 扩容后的大小仍为 10)
    5. `append` 7 个元素, 再 `append` 一个元素, 查看是否正确的扩容. (当前元素为 10, 2 * 10 > 10, 扩容后的大小为 20)
    """
    array = LoopArrayV1()

    # 1
    assert array._data == [None for _ in range(10)]
    assert list(array) == []
    with pytest.raises(IndexError):
        array.popleft()

    # 2
    for i in range(2):
        array.append(i)
    assert array._data == list(range(2)) + [None for _ in range(8)]
    assert list(array) == [0, 1]
    for i in range(2):
        assert i == array.popleft()
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
    assert array._data == [6, 7, 'c'] + [None for _ in range(7)]
    assert list(array) == [6, 7, 'c']

    # 5
    for i in range(7):
        array.append(i)
    array.append(7)
    assert array._data == [6, 7, 'c'] + list(range(8)) + [None for _ in range(9)]
    assert list(array) == [6, 7, 'c'] + list(range(8))
