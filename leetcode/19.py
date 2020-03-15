from .util import ListNode


class Solution:
    """核心方法 - 单指针链表.

    遍历两次, 第一次了解链表长度, 第二次删除元素.

    TODO (完成双指针链表.)
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


class Solution2:
    """核心方法 - 递归."""

    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        # 题目中保证了 `n` 是一个有效的值, 即 n ∈ [1, len + 1).
        index = len(head) - n
        return self._remove(head, 0, index)

    def _remove(self, node: ListNode, cur_index: int,
                target_index: int) -> ListNode:
        """删除节点索引等于目标索引的节点."""
        # 最小情况, 当前节点等于目标节点, 由于题目保证了 `target_index`
        # 是有效的, 所以这个条件肯定先于 `node is None`.
        if cur_index == target_index:
            return node.next

        node.next = self._remove(node.next, cur_index + 1, target_index)
        return node


if __name__ == '__main__':
    """
    1. 删除第一个元素.
    2. 删除最后一个元素.
    3. 删除任意一个中间元素.
    """
    fs = [Solution.removeNthFromEnd, Solution2().removeNthFromEnd]

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
