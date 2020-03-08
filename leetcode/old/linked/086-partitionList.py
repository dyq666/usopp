# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/1 16:39'


class Solution:
    def partition(self, head, x):
        """
        1. 指针移动过程中常用的就是先保存next, 在最后再回到next
        """

        if not head:
            return None

        # 前部分最后面的值，后部分最前面的值
        less_end, greater_start = None, None
        # 标识位-拼接处, needle,next_用于穿梭
        link, needle, next_ = None, head, None

        # 判断是哪种类型的在前面
        start_type = 'less' if head.val < x else 'greater'
        less_start_node = None

        while needle:
            next_ = needle.next

            if needle.val < x:
                """
                1. 如果后部分还没出现过节点, 不做任何改变，针继续向后穿
                2. 如果后部分有, 则让连接处与当前的下一个拼接, 将当前的下一个指向后部分的最前面。
                   如果前部分还没有, 则保存当前为前部分的头节点, 如果有了，则将之前标识位的下一个指向当前的。
                   最后保存标识位(前部分的最后面)
                """
                if greater_start is None:
                    less_end = needle
                else:
                    if not less_end:
                        # 取出needle
                        link.next = needle.next
                        # 直接放到最前面
                        needle.next = greater_start
                        # 标识位
                        less_end = needle
                        less_start_node = needle
                    else:
                        # 取出needle
                        link.next = needle.next
                        # 将needle拼接到前部分
                        less_end.next = needle
                        needle.next = greater_start
                        # 标识位拼接处
                        less_end = needle
            else:
                """
                1. needle.val >= x
                2. 如果是第一个出现的，保存为起始点(greater_start)
                3. 保存标识位(拼接处)
                """
                if greater_start is None:
                    greater_start = needle
                link = needle

            # 后移
            needle = next_

        """
        1. 如果是大值在前，但是后面没有出现过小值, 返回head
        2. 如果是大值在前，后面出现过小值，返回小值的头节点
        3. 如果是小值在前，返回head
        """
        if start_type == 'greater' and less_start_node is None:
            return head

        return head if start_type == 'less' else less_start_node
