# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/1 15:09'


class Solution:
    def reverseList(self, head):
        """
        1. 记录当前指针为last_node
        2. 把下一个指针记录为当前指针
        3. 把当前指针指向last_node
        4. 终止条件：当前指针为空
        """
        last = None
        cur = head

        while cur:
            next_ = cur.next
            cur.next = last
            last = cur

            cur = next_

        return last
