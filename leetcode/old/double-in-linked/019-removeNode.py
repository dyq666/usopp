# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/2 9:20'


class Solution:
    def removeNthFromEnd(self, head, n):
        """
        1. 双指针，一个是一开始启动的，一个是慢一点启动的，通过n来控制什么时候启动第二个needle
        """
        needle = head
        slow_needle = None
        virtual_head = ListNode(None)
        virtual_head.next = head

        while needle:

            needle = needle.next
            if n > 0:
                n -= 1

            if n == 0:
                if slow_needle is None:
                    slow_pre = virtual_head
                    slow_needle = head
                else:
                    slow_pre = slow_needle
                    slow_needle = slow_needle.next

        # 删除节点
        if n == 0:
            slow_pre.next = slow_needle.next

        return virtual_head.next
