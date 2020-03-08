# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/3 20:39'


class Solution:
    def mergeKLists(self, lists):
        """O( nlog(len(lists)) )
        1. queue_index的作用：假设两个元素的优先级相同，那么将会去比较元组中第二个值。
           但是第二个值如果是一个类的实例，可能没重写比较的方法，所以需要一个可以比较的辅助变量来区分。
        2. 初始化队列，将所有链表的头结点入队
        3. 创建最终结果链表的虚拟头结点
        4. 每次从队列中获取优先级最小的元素，用needle去穿针引线
        5. 如果该节点后面还有节点，就将后面的一个节点入队
        """
        from queue import PriorityQueue as PQ

        pq = PQ()
        # 步骤一
        queue_index = 0

        # 步骤二
        for node in lists:
            if node:
                pq.put((node.val, queue_index, node))
                queue_index += 1

        # 步骤三
        dummy = ListNode(None)
        needle = dummy

        # 步骤四
        while pq.queue:
            node = pq.get()[-1]

            needle.next = node
            needle = needle.next

            # 步骤五
            if node.next:
                pq.put((node.next.val, queue_index, node.next))
                queue_index += 1

        return dummy.next
from queue import PriorityQueue