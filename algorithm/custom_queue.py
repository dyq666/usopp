"""
AUTHOR: dyq666
DATE: 2018.7.24
1. 循环动态数组实现的队列 - LoopArrayQueue
"""

from custom_array import LoopDynamicArray


class LoopArrayQueue:
    """
    循环动态数组实现的队列
    方法
    1. 魔法方法: len, str, init
    2. 公有方法: enqueue, dequeue
    """
    def __init__(self):
        """底层数据结构使用自己实现的动态数组"""
        self.__data = LoopDynamicArray()

    def __len__(self):
        """使用动态数组的len方法"""
        return len(self.__data)

    def __str__(self):
        """这里需要访问动态数组类的私有变量"""
        return f'front <- {str(self.__data.get_real_data())} <- ceil'
    
    def dequeue(self):
        """
        出队
        时间复杂度: O(1)
        """
        return self.__data.remove_first()

    def enqueue(self, value):
        """
        入队
        时间复杂度: O(1)
        """
        self.__data.add_last(value)


if __name__ == '__main__':
    # 初始化动态数组实现的栈
    loop_array_queue = LoopArrayQueue()
    print(loop_array_queue)
    
    # 增加元素
    for i in range(6):
        loop_array_queue.enqueue(i)
        print(loop_array_queue)

    # 删除元素
    for i in range(6):
        loop_array_queue.dequeue()
        print(loop_array_queue)
