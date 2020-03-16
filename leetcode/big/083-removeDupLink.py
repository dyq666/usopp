# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/1 15:23'


class Solution:
    def deleteDuplicates(self, head):
        """
        1. needle是一直往前走的
        2. last是保存拼接处的标识，所以当删除一个节点时，last应该不变，否则last应该移动到当期needle的位置
        """

        if not head:
            return None

        last = head
        cur_value = head.val

        needle = head.next

        while needle is not None:
            if needle.val == cur_value:
                last.next = needle.next
            else:
                cur_value = needle.val
                last = needle

            needle = needle.next

        return head
