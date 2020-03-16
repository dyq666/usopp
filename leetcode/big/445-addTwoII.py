# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/1 22:16'


class Solution:
    def addTwoNumbers(self, l1, l2):
        """
        1. 两个栈分别存放l1和来l2的元素
        2. is_carry保存是否有进位, 两个栈分别出栈相加再加进位, 将结果的个位存入新的栈, 然后保存是否有进位
        3. 后续处理，将不是空的栈的元素通过与进位相加继续存入res
        4. 最后如果还有进位, 就把这个1入栈
        5. 出栈建立链表
        """
        stack1, stack2, res = [], [], []

        # 步骤1
        while l1:
            stack1.append(l1.val)
            l1 = l1.next

        while l2:
            stack2.append(l2.val)
            l2 = l2.next

        # 步骤2
        is_carry = 0
        while stack1 and stack2:
            sum1 = stack1.pop() + stack2.pop() + is_carry
            res.append(sum1 % 10)
            is_carry = sum1 // 10

        # 步骤3
        if not stack1 and stack2:
            while stack2:
                sum2 = stack2.pop() + is_carry
                print(sum2, stack2)
                res.append(sum2 % 10)
                is_carry = sum2 // 10
        elif stack1 and not stack2:
            while stack1:
                sum3 = stack1.pop() + is_carry
                res.append(sum3 % 10)
                is_carry = sum3 // 10

        # 步骤四
        if is_carry:
            res.append(is_carry)

        # 步骤五
        head = ListNode(None)
        needle = head

        while res:
            needle.next = ListNode(res.pop())
            needle = needle.next

        return head.next
