from itertools import zip_longest

from libs.tree import BT

class Solution:
    """
    Date: 2018-10-25
    Method: 迭代
    Solution: 后序遍历所有节点, 找出与目标根节点的值并且后序值相同的点.
    """
    def isSubtree(self, s, t):
        nodes = []
        target = [node.val for node in BT.iterpostorder(t)]
        children = {None: []}
        for node in BT.iterpostorder(s):
            children[node] = children[node.left] + children[node.right] + [node.val]
            if node.val == t.val and children[node] == target:
                nodes.append(node)

        for node in nodes:
            if self.isSameTree(node, t):
                return True
        return False

    def isSameTree(self, p, q):
        for n1, n2 in zip_longest(BT.iterdfs(p, False), BT.iterdfs(q, False)):
            v1 = n1 and n1.val
            v2 = n2 and n2.val
            if v1 != v2:
                return False
        return True
