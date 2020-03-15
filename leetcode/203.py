from typing import Optional

from .util import ListNode


class Solution:
    """核心方法 - LinkedList.

    是一道非常典型的链表问题, 既要考虑头尾的问题, 又要处理 `prev`, `cur`
    两个指针移动的问题. 本题必须确保所有元素都被 `cur` 指针指向过, 而删除一个
    元素又需要 `cur` 指针的前一个元素, 即 `prev` 指针. 假设本次没有删除元素,
    则 `prev` 向前移动一位, 删除了则不移动.

    实际上可能 `removeElements2` 的思路更适合链表问题. 因为链表总是需要知道
    前一个索引的元素, 因此遍历 [0, len) 有时候不如遍历 [-1, len - 1) 方便.
    """

    @staticmethod
    def removeElements(head: Optional[ListNode], val: int) -> Optional[ListNode]:
        # 删除第一个元素和其他元素逻辑不同, 因此引入 dummy_head, 使第一个元素也有 `prev`.
        dummy = ListNode(None)
        dummy.next = head

        prev = dummy
        cur = dummy.next

        while cur is not None:
            if cur.val == val:
                # 这里可以清理下 `cur`, 促进垃圾回收.
                prev.next = cur.next
            else:
                prev = prev.next
            cur = prev.next

        return dummy.next

    @staticmethod
    def removeElements2(head: Optional[ListNode], val: int) -> Optional[ListNode]:
        # 删除第一个元素和其他元素逻辑不同, 因此引入 dummy_head, 使第一个元素也有 `prev`.
        dummy = ListNode(None)
        dummy.next = head

        prev = dummy

        while prev.next is not None:
            if prev.next.val == val:
                # 这里可以清理下 `prev.next`, 促进垃圾回收.
                prev.next = prev.next.next
            else:
                prev = prev.next

        return dummy.next


class Solution2:
    """核心方法 - Recursion."""

    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        """删除所有 `head` 链表中值为 `val` 的节点."""
        # 最小情况
        if head is None:
            return None

        # 子问题: 是否移除当前节点
        head.next = self.removeElements(head.next, val)
        return head.next if head.val == val else head


if __name__ == '__main__':
    """
    1. 头结点, 尾结点, 中间结点都有目标值.
    2. 删除空节点.
    3. 连续两个目标节点, 主要是测试 `prev` 移动是否正确.
    """
    val = 1
    fs = [Solution.removeElements, Solution.removeElements2,
          Solution2().removeElements]

    for f in fs:
        # 1
        node = ListNode.from_iterable([1, 2, 3, 1, 4, 1])
        assert list(f(node, val)) == [2, 3, 4]

        # 2
        assert f(None, 1) is None

        node = ListNode.from_iterable([1, 1])
        assert f(node, val) is None
