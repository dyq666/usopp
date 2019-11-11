# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/2 18:01'


class Solution:
    def levelOrder(self, root):
        """
        1. 初始化队列，将头节点保存，由于题目需要根据节点所在的层返回，所以这里队列中的每一项都是一个tuple(节点，层级)，头结点的tuple是（root, 0）
        2. 不断的出队列，知道队列为空，整个树就被遍历完了。
        3.  从队列中获取到当前节点，和节点所在的层级，如果节点是空的就继续出队列，否则进行步骤4和5。
        4.  如果当前的层级是第一次出现，则将结果集中存入一个list，供当前层级存放节点的值。这里使用一个set来判断层级是否是第一次出现，当然还可以使用（len(结果集) - 1 != level ）这种方式，但是不太语义化，本文就没有采取。
        5. 将节点的值存入结果集中对应位置的list中，将左节点，右节点加入队列
        """
        # 步骤1
        from collections import deque
        node_queue = deque()
        node_queue.append((root, 0))

        res, res_set = [], set()

        # 步骤2
        while node_queue:
            # 步骤三
            node, level = node_queue.popleft()
            if node:
                # 步骤四
                if level not in res_set:
                    res_set.add(level)
                    res.append([])
                # 步骤五
                res[level].append(node.val)
                node_queue.append((node.left, level + 1))
                node_queue.append((node.right, level + 1))

        return res

    def levelOrder02(self, root):
        """使用res长度的判断来代替set"""
        from collections import deque
        node_queue = deque()
        node_queue.append((root, 0))

        res = []

        # 步骤3
        while node_queue:
            node, level = node_queue.popleft()
            # 步骤四
            if node:
                if len(res) - 1 != level:
                    res.append([])
                res[level].append(node.val)
                node_queue.append((node.left, level + 1))
                node_queue.append((node.right, level + 1))

        return res
