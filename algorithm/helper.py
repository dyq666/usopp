"""
AUTHOR: dyq666
DATE: 2018.7.24
提供一些创建数据结构时需要用的方法
1. 左闭右闭的range
2. 左闭右闭+逆向的range
3. 将单字符变为双字符
4. 交换数组中两个索引位置
"""

def closed_range(l, r, step=1):
    """提供左闭右闭合的range"""
    return range(l, r+1, step)


def closed_reversed_range(r, l, step=-1):
    """提供左闭右闭的逆向range"""
    return range(r, l-1, step)


def swap_two_ele(nums, ele1, ele2):
    """
    交换数组中索引ele1和ele2的位置
    """
    assert 0 <= ele1 < len(nums) and 0 <= ele2 < len(nums), "索引超出了数组的范围"

    nums[ele1], nums[ele2] = nums[ele2], nums[ele1]
