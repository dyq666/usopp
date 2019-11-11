# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/2 18:35'


class Solution:
    def zigzagLevelOrder(self, root):
        """
        1. 在102基础上有很小的变化
        2. 应该是属于偷鸡摸狗方式, 以后解决
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

        return [item if i % 2 == 0 else list(reversed(item)) for i, item in enumerate(res)]
