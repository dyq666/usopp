# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/2 9:37'


class Solution:
    def reverseKGroup(self, head, k):
        """
        1. 024的问题的一般化
        2. 注意依靠node_nums来判断什么时候开始要交换了
        3. 交换时需要一个前置位(link)
        """
        virtual_head = ListNode(None)
        virtual_head.next = head
        needle = head

        nodes, node_nums = [None] * (k + 1), 0
        link = virtual_head

        while needle:
            next_ = needle.next

            node_nums += 1
            nodes[node_nums] = needle

            if node_nums == k:
                for i in range(k, 0, -1):
                    if i == k:
                        link.next = nodes[i]
                    else:
                        nodes[i + 1].next = nodes[i]
                nodes[1].next = next_
                link = nodes[1]
                node_nums = 0

            needle = next_

        return virtual_head.next
