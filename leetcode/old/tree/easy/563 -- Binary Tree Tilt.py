from libs.tree import BT

class Solution:
    """
    Date: 2018-10-05
    Method: 迭代
    """
    def findTilt(self, root):
        self.tilt = 0
        self._sum(root)
        return self.tilt

    def _sum(self, node):
        if not node:
            return 0

        left = self._sum(node.left)
        right = self._sum(node.right)
        self.tilt += abs(left - right)
        return left + right + node.val

class Solution02:
    """
    Date: 2018-10-25
    Method: 迭代
    Solution: 后序遍历, dict 存储以节点为根的所有节点的和
    """
    def findTilt(self, root):
        sums = {None: 0}
        tilt = 0
        for node in BT.iterpostorder(root):
            sums[node] = node.val + sums[node.left] + sums[node.right]
            tilt += abs(sums[node.left] - sums[node.right])
        return tilt
