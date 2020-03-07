from typing import Optional


class ListNode:

    def __init__(self, x: Optional[int]):
        self.val = x
        self.next = None


class Solution:

    @staticmethod
    def addTwoNumbers(l1: ListNode, l2: ListNode) -> Optional[ListNode]:
        """核心方法 - 链表.

        主链表 (`dummy`) 的停止条件: `l1` 和 `l2` 都走到头, 且没有进位.
        """
        has_carry = False  # 是否有进位
        dummy = ListNode(None)
        needle = dummy

        while l1 or l2 or has_carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0
            l1 = l1 and l1.next
            l2 = l2 and l2.next

            total = v1 + v2 + has_carry
            has_carry = total >= 10
            needle.next = ListNode(total % 10)
            needle = needle.next

        return dummy.next
