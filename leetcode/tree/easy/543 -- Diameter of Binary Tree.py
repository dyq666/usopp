from libs.tree import BT

class Solution:
    """
    Date: 2018-10-06
    Method: 递归
    Solution: 深度
    """
    def diameterOfBinaryTree(self, root):
        self.diameter = 0
        self._depth(root)
        return self.diameter

    def _depth(self, node):
        if not node:
            return 0

        left_depth = self._depth(node.left)
        right_depth = self._depth(node.right)
        self.diameter = max(self.diameter, left_depth+right_depth)
        return 1 + max(left_depth, right_depth)

class Solution02:
    """
    Date: 2018-10-25
    Method: 迭代
    Solution: 后序遍历, dict 存储节点的最大深度
    """
    def diameterOfBinaryTree(self, root):
        depths = {None: 0} # 空节点的深度
        max_diameter = 0
        for node in BT.iterpostorder(root):
            depths[node] = 1 + max(depths[node.left], depths[node.right])
            max_diameter = max(max_diameter, depths[node.left] + depths[node.right])
        return max_diameter

