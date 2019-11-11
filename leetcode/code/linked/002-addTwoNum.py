# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/1 22:25'


class Solution:
    def addTwoNumbers(self, l1, l2):
        """
        1. 与445基本相同，把栈全都替换成队列
        """
        from collections import deque

        deque1, deque2, res = deque(), deque(), deque()

        # 步骤1
        while l1:
            deque1.append(l1.val)
            l1 = l1.next

        while l2:
            deque2.append(l2.val)
            l2 = l2.next

        # 步骤2
        is_carry = 0
        while deque1 and deque2:
            sum1 = deque1.popleft() + deque2.popleft() + is_carry
            res.append(sum1 % 10)
            is_carry = sum1 // 10

        # 步骤3
        if not deque1 and deque2:
            while deque2:
                sum2 = deque2.popleft() + is_carry
                res.append(sum2 % 10)
                is_carry = sum2 // 10
        elif deque1 and not deque2:
            while deque1:
                sum3 = deque1.popleft() + is_carry
                res.append(sum3 % 10)
                is_carry = sum3 // 10

        # 步骤四
        if is_carry:
            res.append(is_carry)

        # 步骤五
        head = ListNode(None)
        needle = head

        while res:
            needle.next = ListNode(res.popleft())
            needle = needle.next

        return head.next
