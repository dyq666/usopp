"""
AUTHOR: dyq666
DATE: 2018.7.24
1. 动态数组类 - DynamicArray
2. 循环动态数组类 - LoopDynamicArray
"""

from random import randint

from decorator import index_valid, size_change, non_empty


class LoopDynamicArray:
    """
    循环动态数组
    与动态数组相比主要有以下几点区别:
    1. 需要两个指针front和last来记录数组的头和尾, 这里设计的last指针指向下一个插入的位置, 也就是数组的尾巴+1
    2. 在修改索引时, 例如index+1等操作需要进行除余的处理
    3. 数组满的情况是, last不断往前走, 直到和front重叠, 也就是下一个要插入的位置是数组的起始位置, 但是由于数组为空的情况, 头和尾也是这种关系, 因此还需要判断数组是否有元素
    方法
    1. 魔法方法: len, str, init
    2. 公有方法: add_last, remove_first
    3. 私有方法: is_full, get_capacity, resize, get_next_index, get_cur_real_index 
    """
    def __init__(self, capacity=10):
        """设置头尾两个指针"""
        self.__data = [None] * capacity
        self._size = 0 # 一个下划线的原因是装饰器需要使用这个变量
        self.__front = 0
        self.__last = 0

    def __len__(self):
        return self._size

    def get_real_data(self):
        """返回一个外界可用的从front->last的数组, 也就是对外界隐藏我们是用循环实现的"""
        return [self.__data[self.__get_cur_real_index(i+self.__front)] for i in range(self._size)]

    @size_change(1)
    def add_last(self, value):
        """
        功能: 在数组末尾增加一个元素
        时间复杂度: O(1)
        1. 数组满了, 需要扩容
        2. 数组没满, 在last的位置放置元素, 并将last置于下个正确的索引
        """
        # 1
        if self.__is_full():
            self.__resize(self.__get_capacity() * 2)

        # 2
        self.__data[self.__last] = value
        self.__last = self.__get_next_index(self.__last)
    
    @non_empty
    def remove_first(self):
        """
        功能: 在数组开头增加一个元素
        时间复杂度: O(1)
        1. 保存即将删除的头位置的元素
        2. 将头位置的值变为None, 将front置于下个正确的索引
        3. 维护数组的大小
        4. 如果数组大小比容量的1/3还小则缩容两倍。又因为容量必须大于1, 因此还需要满足缩容两倍后大于0
        5. 返回删除的值
        """
        # 1.
        remove_value = self.__data[self.__front]

        # 2.
        self.__data[self.__front] = None
        self.__front = self.__get_next_index(self.__front)

        # 3.
        self._size -= 1
        
        # 4.
        if self._size < self.__get_capacity() // 3 and self.__get_capacity() // 2 > 0:
            self.__resize(self.__get_capacity() // 2)

        # 5.
        return remove_value

    def __get_capacity(self):
        """返回动态数组的容量"""
        return len(self.__data)

    def __is_full(self):
        """如果头尾指向一个元素并且有元素"""
        return self.__front == self.__last and self._size

    def __get_next_index(self, cur_index):
        """
        返回下一个的索引的正确位置, 代替类似index+1的操作
        举例: 
            - capacity=9, 当前索引是[0, 7], 下个索引理论值为[1, 8], %9后仍是[1, 8]
            - capacity=9, 当前索引是8, 下个索引理论值为9, %9后变为0
            - 正好完成了在[0, 8]范围内的循环索引
        """
        return (cur_index + 1) % self.__get_capacity()

    def __get_cur_real_index(self, cur_index):
        """
        配合__get_next_index使用
        """
        return self.__get_next_index(cur_index - 1)

    def __resize(self, new_capacity):
        """
        更改数组的容量
        1. 生成一个新的数组
        2. 将原来数组中所有元素赋值到新数组
           - 新数组中的范围是[0, new_capacity-1]
           - 而老数组的范围是[front, last-1], 同时需要考虑循环数组的索引问题
        3. 重置头尾索引
        4. 将原数组变为新数组
        """
        # 1. 
        new_data = [None] * new_capacity

        # 2.
        for i in range(self._size):
            # 老数组的对应的索引值
            old_data_index = self.__front + i
            # 老数组对应的索引值的真实值
            new_data[i] = self.__data[self.__get_cur_real_index(old_data_index)]

        # 3.
        self.__front = 0
        self.__last = self._size

        # 4.
        self.__data = new_data


if __name__ == '__main__':
    # 动态数组的测试
    # # 初始化动态数组
    # dynamic_array = DynamicArray()
    # print(dynamic_array)
    
    # # 增加元素
    # for i in range(11):
    #     dynamic_array.add(len(dynamic_array), i)
    #     print(dynamic_array)

    # # 删除元素
    # for i in range(11):
    #     dynamic_array.remove(len(dynamic_array)-1)
    #     print(dynamic_array)

    # 循环动态数组测试
    # 初始化循环动态数组
    loop_dynamic_array = LoopDynamicArray()
    print(loop_dynamic_array)

    # 随机进行20次操作
    for i in range(21):

        operator_random = randint(-1, 4)
        operator = "remove" if operator_random < 0 else "add"
        operator = operator.center(6)
        value_random = randint(0, 9)

        if operator == "remove":
            loop_dynamic_array.remove_first()
        else:
            loop_dynamic_array.add_last(value_random)
        print(loop_dynamic_array, f"Operator: {operator} {value_random}")
