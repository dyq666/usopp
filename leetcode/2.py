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
        dummy = ListNode(None)
        needle = dummy
        has_carry = False  # 是否有进位

        while l1 is not None or l2 is not None:
            v1 = 0 if l1 is None else l1.val
            v2 = 0 if l2 is None else l2.val
            l1 = l1 and l1.next
            l2 = l2 and l2.next

            total = v1 + v2 + int(has_carry)
            has_carry = total >= 10
            needle.next = ListNode(total % 10)
            needle = needle.next

        # 当两个链表都走到头时, 依然可能有进位需要处理.
        if has_carry:
            needle.next = ListNode(1)

        return dummy.next
