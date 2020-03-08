# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/1 22:50'


class Solution:
    def oddEvenList(self, head):
        """
        1. 86题的简单版本
        2. 改动点在于
           1. 不用判断返回哪个节点, 都返回head
           2. 逻辑清晰，先奇后偶循环
        """
        even_link = None
        even_start = None
        odd_end = None

        needle = head

        is_odd = True

        while needle:
            next_ = needle.next

            if is_odd:
                if not odd_end:
                    odd_end = needle
                else:
                    even_link.next = needle.next
                    odd_end.next = needle
                    needle.next = even_start
                    odd_end = needle
                is_odd = False
            else:
                if not even_start:
                    even_start = needle
                even_link = needle
                is_odd = True

            needle = next_

        return head
