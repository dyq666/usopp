# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/1 15:13'


class Solution:
    def mergeTwoLists(self, l1, l2):
        """
        1. 链表问题，总会有几个变量保存指针的某些节点（比如头结点），还有其他变量负责在链表中穿梭
        2. 这道问题与归并排序的合并过程类似
        3. 当1和2都的针都到头了就结束
        """

        res_head = ListNode(0)
        res_node = res_head

        node1, node2 = l1, l2

        while node1 is not None or node2 is not None:
            change = None

            if node1 is None:
                change = "node2"
            elif node2 is None:
                change = "node1"
            elif node1.val <= node2.val:
                change = "node1"
            else:
                change = "node2"

            if change == "node2":
                res_node.next = node2
                node2 = node2.next
            else:
                res_node.next = node1
                node1 = node1.next

            res_node = res_node.next

        return res_head.next
