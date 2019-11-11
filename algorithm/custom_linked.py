"""
AUTHOR: dyq666
DATE: 2018.7.24
1. 链表的节点 - Node
2. 链表 - LinkedList
3. 头尾链表 - TailLinkedList
"""

from decorator import index_valid, size_change, non_empty


class Node:
    """实现链表的节点"""
    def __init__(self, value=None, next_node=None):
        self.value = value
        self.next_node = next_node

    def __str__(self):
        return str(self.value)


class LinkedList:
    """
    链表
    概述:
    1. 链表的核心是固定针头(头节点), 通过一线从针头开始到查找需要修改的地方
    2. 这里的链表主要实现了增加元素和删除元素
    3. 由于只有在头部进行操作时间复杂度是O(1)的因此提供了这两个方式
    方法:
    魔法方法: init, len, str
    公有方法: add, remove, add_first, remove, remove_first
    """
    def __init__(self):
        """使用虚拟头节点, 减少了很多在头节点操作的代码"""
        self.dummy_head = Node()
        self._size = 0
    
    def __len__(self):
        return self._size

    def __str__(self):
        res = ["dummy_head"]
        needle = self.dummy_head
        for _ in range(self._size):
            needle = needle.next_node
            res.append(str(needle.value))
        return " -> ".join(res)

    @index_valid('0', 'self._size')
    @size_change(1)
    def add(self, index, value):
        """
        功能: 在index的位置插入值value
        概述:
        1. 需要找到插入位置的前一个值prev_node, 和后一个值next_node = prev_node.next_node
        2. 插入后变为prev_node -> 插入的节点 -> prev_node.next
        实现:
        1. 从虚拟头节点开始, 往后找index个值, 找到prev_node
        2. 找到next_node
        3. 插入节点
        """
        # 1.
        prev_node = self.dummy_head
        for _ in range(index):
            prev_node = prev_node.next_node

        # 2.
        next_node = prev_node.next_node

        # 3.
        prev_node.next_node = Node(value, next_node)      
    
    @index_valid('0', 'self._size-1')
    @size_change(-1)
    def remove(self, index):
        """
        功能: 在index的位置的元素
        概述:
        1. 需要找到插入位置的前一个值prev_node, 和后一个值next_node = prev_node.next_node.next_node(注意这里与加入不一样)
        2. 插入后变为prev_node -> prev_node.next
        实现:
        1. 从虚拟头节点开始, 往后找index个值, 找到prev_node
        2. 保存删除值
        3. 设置next_node
        4. 删除节点
        5. 返回删除值
        """
        # 1.
        prev_node = self.dummy_head
        for _ in range(index):
            prev_node = prev_node.next_node
        
        # 2. 
        remove_value = prev_node.next_node.value

        # 3.
        next_node = prev_node.next_node.next_node

        # 4.
        prev_node.next_node = next_node

        # 5.
        return remove_value

    def add_first(self, value):
        """在开头增加元素"""
        return self.add(0, value)

    def remove_first(self):
        """删除第一个元素"""
        return self.remove(0)


class TailLinkedList:
    """
    链表
    概述:
    1. 为了满足队列的要求, 额外设置了一个指针来负责从链表的尾部进行操作
    2. 由于是满足队列的要求, 因此只实现两个核心功能从头删, 从尾加
    方法:
    魔法方法: init, len, str
    公有方法: add_last, remove_first
    """
    def __init__(self):
        self.dummy_head = Node()
        self.tail = self.dummy_head
        self._size = 0

    def __len__(self):
        return self._size

    def __str__(self):
        res = ["dummy_head"]
        needle = self.dummy_head
        for _ in range(self._size):
            needle = needle.next_node
            res.append(str(needle.value))
        res.append("<- tail")
        return " -> ".join(res)

    @size_change(1)
    def add_last(self, value):
        """使用尾指针连接, 维护尾指针"""
        self.tail.next_node = Node(value)
        self.tail = self.tail.next_node

    @non_empty
    @size_change(-1)
    def remove_first(self):
        """删除虚拟头节点的下一个节点即可, 如果尾节点指向这个指针(这种情况是尾节点指向最后一个指针), 他也跟着去世了, 因此要重置尾节点"""
        remove_value = self.dummy_head.next_node.value
        
        # 删除节点
        self.dummy_head.next_node = self.dummy_head.next_node.next_node

        # 维护尾节点
        if self.dummy_head.next_node is None:
            self.tail = self.dummy_head

        return remove_value


if __name__ == '__main__':
    # 简单的链表测试
    # 初始化简单的链表
    # linked_list = LinkedList()
    # print(linked_list)
    
    # # 增加元素
    # for i in range(10):
    #     linked_list.add_first(i)
    #     print(linked_list)

    # # 删除元素
    # for i in range(10):
    #     linked_list.remove_first()
    #     print(linked_list)

    # 头尾链表测试
    # 初始化头尾链表
    tail_linked_list = TailLinkedList()
    print(tail_linked_list)
    
    # 增加元素
    for i in range(10):
        tail_linked_list.add_last(i)
        print(tail_linked_list)

    # 删除元素
    for i in range(10):
        tail_linked_list.remove_first()
        print(tail_linked_list)
