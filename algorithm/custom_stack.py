"""
AUTHOR: dyq666
DATE: 2018.7.24
1. 动态数组实现的栈 - ArrayStack
"""

from custom_array import DynamicArray


class ArrayStack:
    """
    动态数组实现的栈
    方法
    1. 魔法方法: len, str, init
    2. 公有方法: push, pop
    """
    def __init__(self):
        """底层数据结构使用自己实现的动态数组"""
        self.__data = DynamicArray()

    def __len__(self):
        """使用动态数组的len方法"""
        return len(self.__data)

    def __str__(self):
        """这里需要访问动态数组类的私有变量"""
        return f'{str(self.__data._DynamicArray__data[:len(self.__data)])} <- top'
    
    def pop(self):
        """
        出栈
        时间复杂度: O(1)
        """
        return self.__data.remove(len(self.__data)-1)

    def push(self, value):
        """
        入栈
        时间复杂度: O(1)
        """
        self.__data.add(len(self.__data), value)


if __name__ == '__main__':
    # 初始化动态数组实现的栈
    array_stack = ArrayStack()
    print(array_stack)
    
    # 增加元素
    for i in range(6):
        array_stack.push(i)
        print(array_stack)

    # 删除元素
    for i in range(6):
        array_stack.pop()
        print(array_stack)
