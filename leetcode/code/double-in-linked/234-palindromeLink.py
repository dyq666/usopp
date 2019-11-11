# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/2 11:50'


class Solution:
    def isPalindrome(self, head):
        """
        1. 计算链表长度
        2. 计算后部分的起始位(分为奇数偶数两种情况)
        3. 翻转前部分的链表(分为奇数偶数情况)
        4. 翻转结束准备开始比较
        5. 比较
        """
        # 步骤1
        needle_count, count = head, 0

        while needle_count:
            count += 1
            needle_count = needle_count.next

        if count == 1 or count == 0:
            return True

        # 步骤2
        after_start = (count // 2) + 1 if count % 2 == 0 else (count // 2) + 2

        front, needle, cur_count = None, head, 0

        virtual_head = ListNode(None)
        virtual_head.next = head
        is_comp = False
        last = None

        while needle:
            next_ = needle.next
            cur_count += 1

            # 步骤3
            if cur_count < after_start:
                if count % 2 != 0 and cur_count == (count // 2) + 1:
                    needle = next_
                    continue
                if cur_count > 1:
                    needle.next = last
                last = needle
            # 步骤四
            elif cur_count == after_start:
                head.next = needle
                virtual_head.next = last
                is_comp = True
                front = virtual_head.next
            # 步骤五
            if is_comp:
                print(front.val, needle.val)
                if front.val != needle.val:
                    return False
                front = front.next

            needle = next_

        return True
