from typing import List, Optional

from util import PrioQueue

from .util import ListNode


class Solution:
    """核心方法 - LinkedList.

    这个解决办法在 LeetCode 上是 Time Limit Exceeded. 原因: 假设有 1000 个链表,
    每轮都会查看这 1000 个链表中第一个节点的值, 然后只有一个链表可以向前移动, 也就是
    只有一个值被充分利用了, 其他 999 个值下轮还得再看一遍.
    """

    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        dummy = ListNode(None)
        needle = dummy

        while any(lists):
            # 利用 tuple 比较的特性, 比较 value 的同时返回索引.
            v, i = min((node.val, i) for i, node in enumerate(lists) if node)
            lists[i] = lists[i].next
            lists = [node for node in lists if node]
            needle.next = ListNode(v)
            needle = needle.next

        return dummy.next


class Solution2:
    """核心方法 - PriorityQueue."""

    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        dummy = ListNode(None)
        needle = dummy

        pq = PrioQueue.from_pairs((node.val, node) for node in lists if node)
        while pq:
            node = pq.get()
            if node.next:
                pq.put(node.next.val, node.next)
            needle.next = node
            needle = needle.next

        return dummy.next


if __name__ == '__main__':
    """
    1. 合并三个按顺序的链表 (按顺序指的是头尾相连所有链表就可以得到最终结果).
    2. 合并三个普通的链表.
    """
    fs = [Solution().mergeKLists, Solution2().mergeKLists]

    for f in fs:
        # 1
        l1 = ListNode.from_iterable([1, 2, 3])
        l2 = ListNode.from_iterable([4])
        l3 = ListNode.from_iterable([5, 6, 7])
        assert list(f([l1, l2, l3])) == list(range(1, 8))

        # 2
        l1 = ListNode.from_iterable([1, 4, 5])
        l2 = ListNode.from_iterable([2, 3, 7])
        l3 = ListNode.from_iterable([0, 6, 8, 9])
        assert list(f([l1, l2, l3])) == list(range(10))
