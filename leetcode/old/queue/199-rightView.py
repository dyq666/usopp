# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/2 18:47'


class Solution:
    def rightSideView(self, root):
        """
        1. 102问题的扩展
        2. 每层都只返回最后一个
        """
        from collections import deque
        node_queue = deque()
        node_queue.append((root, 0))

        res, res_set = [], set()

        while node_queue:
            node, level = node_queue.popleft()
            if node:
                if level not in res_set:
                    res_set.add(level)
                    res.append([])
                res[level].append(node.val)
                node_queue.append((node.left, level + 1))
                node_queue.append((node.right, level + 1))

        return [item[-1] for item in res]
