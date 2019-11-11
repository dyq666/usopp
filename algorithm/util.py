__all__ = (
    'swap_two_ele',
)


def swap_two_ele(array, index_1, index_2):
    len_ = len(array)
    assert 0 <= index_1 < len_ and 0 <= index_2 < len_, '索引超出了数组的范围'

    array[index_1], array[index_2] = array[index_2], array[index_1]
