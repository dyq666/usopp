from typing import Optional

from .util import ListNode


class Solution:
    """核心方法 - LinkedList."""

    def mergeTwoLists(self, l1: Optional[ListNode], l2: Optional[ListNode]
                      ) -> Optional[ListNode]:
        dummy = ListNode(None)
        needle = dummy

        while l1 or l2:
            v1 = l1.val if l1 else float('inf')
            v2 = l2.val if l2 else float('inf')
            if v1 < v2:
                l1 = l1 and l1.next
            else:
                l2 = l2 and l2.next
            needle.next = ListNode(min(v1, v2))
            needle = needle.next

        return dummy.next


if __name__ == '__main__':
    """
    1. l1, l2 都为空. l1, l2 其中之一为空.
    2. l1 比 l2 长, l2 比 l1 长, 并且其中一条链表中所有元素都小于另一条链表.
    3. 二者长度相同.
    """
    f = Solution().mergeTwoLists

    # 1
    assert f(None, None) is None
    assert list(f(ListNode.from_iterable([1]), None)) == [1]
    assert list(f(None, ListNode.from_iterable([1]))) == [1]

    # 2
    l1 = ListNode.from_iterable([1, 2, 3])
    l2 = ListNode.from_iterable([4])
    assert list(f(l1, l2)) == [1, 2, 3, 4]
    l1 = ListNode.from_iterable([4])
    l2 = ListNode.from_iterable([1, 2, 3])
    assert list(f(l1, l2)) == [1, 2, 3, 4]

    # 3
    l1 = ListNode.from_iterable([1, 4, 5])
    l2 = ListNode.from_iterable([2, 3, 10])
    assert list(f(l1, l2)) == [1, 2, 3, 4, 5, 10]
