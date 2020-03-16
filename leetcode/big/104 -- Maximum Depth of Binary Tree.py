from libs.tree import BT

class Solution:
    """
    Date: 2018-10-09
    Update: 2018-10-11
    Method: 递归
    """
    def maxDepth(self, root):
        if not root:
            return 0

        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))

class Solution02:
    """
    Date: 2018-10-09
    Update: 2018-10-11
    Method: 迭代
    """
    def maxDepth(self, root):
        return sum(1 for _ in BT.iterlevel(root))
