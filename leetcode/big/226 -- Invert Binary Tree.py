from libs.tree import BT

class Solution:
    """
    Date: 2018-10-03
    Method: 递归
    Solution: dfs
    """
    def invertTree(self, root):
        if not root:
            return

        self.invertTree(root.left)
        self.invertTree(root.right)
        root.left, root.right = root.right, root.left
        return root

class Solution02:
    """
    Date: 2018-10-09
    Update: 2018-10-11
    Method: 迭代
    Solution: dfs
    """
    def invertTree(self, root):
        for node in BT.iterdfs(root):
            node.left, node.right = node.right, node.left
        return root
