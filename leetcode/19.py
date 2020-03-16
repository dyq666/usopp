from .util import ListNode


class Solution:
    """核心方法 - 链表.

    `removeNthFromEnd` 单指针遍历两次, 第一次了解链表长度, 第二次删除元素.
    `removeNthFromEnd2` 双指针遍历一次, 两个指针相差 `n` 的距离`.
    """

    @staticmethod
    def removeNthFromEnd(head: ListNode, n: int) -> ListNode:
        # 题目中保证了 `n` 是一个有效的值, 即 n ∈ [1, len + 1).
        index = len(head) - n

        dummy = ListNode(None, head)
        needle = dummy
        # 找 `index` 前一个位置的元素
        for _ in range(index):
            needle = needle.next
        needle.next = needle.next.next
        return dummy.next

    @staticmethod
    def removeNthFromEnd2(head: ListNode, n: int) -> ListNode:
        dummy = ListNode(None, head)

        # fast 和被删除的节点之间的距离相差 n, 但由于删除节点需要找到
        # 前一个元素, 因此让 slow 指向 dummy.
        fast, slow = head, dummy
        step = 0

        while fast is not None:
            if step >= n:
                slow = slow.next
            fast = fast.next
            step += 1

        # 题目中保证了 `n` 是一个有效的值, 即 n ∈ [1, len + 1), 所以一定能删除某个节点.
        slow.next = slow.next.next
        return dummy.next


class Solution2:
    """核心方法 - 递归."""

    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        # 题目中保证了 `n` 是一个有效的值, 即 n ∈ [1, len + 1).
        index = len(head) - n
        return self._remove(head, index)

    def _remove(self, node: ListNode, target_index: int) -> ListNode:
        """删除节点索引等于目标索引的节点."""
        # 最小情况, 目标索引为 0, 由于题目保证了 `target_index` 是有效的,
        # 所以这个条件肯定先于 `node is None`.
        if target_index == 0:
            return node.next

        node.next = self._remove(node.next, target_index - 1)
        return node


if __name__ == '__main__':
    """
    1. 删除第一个元素.
    2. 删除最后一个元素.
    3. 删除任意一个中间元素.
    """
    fs = [Solution.removeNthFromEnd, Solution.removeNthFromEnd2,
          Solution2().removeNthFromEnd]

    for f in fs:
        # 1
        node = ListNode.from_iterable([1, 2, 3])
        assert list(f(node, 3)) == [2, 3]

        # 2
        node = ListNode.from_iterable([1, 2, 3])
        assert list(f(node, 1)) == [1, 2]

        # 3
        node = ListNode.from_iterable([1, 2, 3])
        assert list(f(node, 2)) == [1, 3]
