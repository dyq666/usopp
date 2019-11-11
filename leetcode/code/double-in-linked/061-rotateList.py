# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/2 10:28'


class Solution:
    def rotateRight(self, head, k):
        """ - 理论上应该用双指针
        1. 遍历一遍链表，保存所有节点。
           节点按起始索引为1进行存储。
        2. 由于需要除以节点的个数，所以在最开始保证head不为空(不能除以0)
        3. k根据节点个数求余, k只有在[1...len-1]的范围才翻转
        4. 开始翻转
           k=0时：相当于不用翻转，返回head
           k!=0时：设被翻转的节点为a, 将a前一个节点接None，最后一个节点接第一个节点，返回a
        """
        # 步骤二
        if not head:
            return

        needle = head

        # 步骤一
        nodes = [None]

        while needle:
            nodes.append(needle)
            needle = needle.next

        # 步骤三
        k = k % (len(nodes) - 1)

        if k == 0:
            return head
        else:
            nodes[-(k + 1)].next = None
            nodes[-1].next = nodes[1]
            return nodes[-k]
