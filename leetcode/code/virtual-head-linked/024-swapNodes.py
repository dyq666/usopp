# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/2 8:38'


class Solution:
    def swapPairs(self, head):
        """
        1. 需要虚拟头，因为前两个节点交换时，需要头结点前面要有一个节点
        2. 总共需要两个额外的标记位，当前节点的前一个节点和前一个前一个节点
        3. 在node_nums等于0时记录前一个前一个, 1时记录前一个，2时开始交换，交换完之后相当于node_nums为0了所以保存前一个前一个节点
        """
        virtual_head = ListNode(None)
        virtual_head.next = head
        node_nums = 0
        needle = head

        pre_pre, pre = virtual_head, None

        while needle:
            next_ = needle.next
            node_nums += 1

            if node_nums == 1:
                pre = needle
            elif node_nums == 2:
                # 交换节点
                pre_pre.next = needle
                needle.next = pre
                pre.next = next_

                # 记录前一个前一个节点
                pre_pre = pre
                node_nums = 0

            needle = next_

        return virtual_head.next
