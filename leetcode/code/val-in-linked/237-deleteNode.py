# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/2 8:57'


class Solution:
    def deleteNode(self, node):
        """
        1. 需要改变节点中的值
        """
        if node is None:
            return

        if node.next == None:
            node = None
            return

        node.val = node.next.val
        node.next = node.next.next
