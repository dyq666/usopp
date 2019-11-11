"""
AUTHOR: dyq666
DATE: 2018.7.26
1. 树的节点 - Node
2. 二分搜索树 - BST
"""

from collections import deque


class Node:
    """二分搜索树的节点"""
    def __init__(self, key, value):
        """为了更好的拓展到set和dict这里在节点中保存了两个值"""
        self.key = key
        self.value = value
        self.left = None
        self.right = None
    
    def __str__(self):
        return str(self.value)


class BST:
    """
    二分搜索树
    概述:
    1. 树中常使用递归的方法，因此一个方法通常有一个公有方法提供给外界, 一个私有方法用于递归
    2. 二叉树从简单到难的操作是：查询, 增加, 层序, 删除
    3. 删除节点需要通过学习查询最值, 删除最值, 删除任意节点的顺序
    4. 这里没有实现前中后遍历, 因为使用递归的方式比较简单
    方法:
    魔法方法: init, len, str
    公有方法: add, contains, level_order, minimum, maximum
             remove_min, remove_max
    """
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    def __str__(self):
        """提供比较树形的显示方式。"""
        pass
    
    def add(self, k, v):
        """
        功能: 增加一个节点
        """
        self.root = self.__add(self.root, k, v)

    def __add(self, node, k, v):
        """
        功能: 在以node为根节点的二插搜索树中增加一个节点(递归)
        1. 如果为空, 则返回一个新的创建的节点, 总数+1
        2. 如果相等, 则直接更新节点的值, 如果小于值则走左, 大于值则走右
        """
        # 1.
        if node is None:
            self._size += 1
            return Node(k, v)
        
        # 2.
        if node.key == k:
            node.value = v
        elif node.key < k:
            node.left = self.__add(node.left, k, v)
        elif node.key > k:
            node.right = self.__add(node.right, k, v)

        return node

    def contains(self, k):
        """查询是否有k"""
        return self.__contains(self.root, k)
        
    def __contains(self, node, k):
        """查询与增加类似, 但是由于不生成新的节点, 因此有小的差距"""
        if node is None:
            return False

        if node.key == k:
            return True
        elif node.key < k:
            self.__contains(node.left, k)
        elif node.key > k:
            self.__contains(node.right, k)

    def level_order(self):
        """层序遍历, 使用队列"""
        q = deque()
        q.append(self.root)

        while q:
            cur_node = q.popleft()
            print(cur_node.value)

            if cur_node.left is not None:
                q.append(cur_node.left)
            if cur_node.right is not None:
                q.append(cur_node.right)

    def minimum(self):
        """获取最小值的节点"""
        node = self.__minimum(self.root)
        return node.key

    def __minimum(self, node):
        """一直往左节点找, 如果当前节点没有左节点则结束查找"""
        if node.left is None:
            return node
        return self.__minimum(node.left)

    def maximum(self):
        """获取最大值的节点"""
        node = self.__maximum(self.root)
        return node.key

    def __maximum(self, node):
        """一直往右节点找, 如果当前节点没有左节点则结束查找"""
        if node is None:
            return node
        return self.__maximum(node.right)

    def remove_min(self):
        if self.root is not None:
            self.root = self.__remove_min(self.root)

    def __remove_min(self, node):
        """删除最小值, 就需要返回最小值的右节点, 然后让删除节点的父节点的左孩子连接返回的右节点"""
        if node.left is None:
            rchild = node.right
            node.right = None
            self._size -= 1
            return rchild
        node.left = self.__remove_min(node.left)
        return node

    def remove_max(self):
        if self.root is not None:
            self.root = self.__remove_max(self.root)

    def __remove_max(self, node):
        """删除最大值, 就需要返回最大值的左节点, 然后让删除节点的父节点的右孩子连接返回的左节点"""
        if node.right is None:
            lchild = node.left
            node.left = None
            self._size -= 1
            return lchild
        node.right = self.__remove_max(node.right)
        return node

    def remove(self, k):
        self.root = self.__remove(self.root, k)

    def __remove(self, node, k):
        pass
