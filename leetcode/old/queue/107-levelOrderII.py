# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/2 18:20'


class Solution:
    def levelOrderBottom(self, root):
        """
        1. 102问题上加一个翻转
        """
        from collections import deque
        nodes = deque()
        nodes.append((root, 0))

        res, res_set = [], set()

        while nodes:
            node, level = nodes.popleft()
            if node:
                if level not in res_set:
                    res_set.add(level)
                    res.append([])
                res[level].append(node.val)
                nodes.append((node.left, level + 1))
                nodes.append((node.right, level + 1))

        return list(reversed(res))
