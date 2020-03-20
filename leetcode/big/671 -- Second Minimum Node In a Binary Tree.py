from libs.tree import BT


class Solution:
    """
    Date: 2018-10-10
    Method: 迭代
    Solution: dfs
    """

    def findSecondMinimumValue(self, root):
        second = float('inf')
        for node in BT.iterdfs(root):
            if root.val < node.val:
                second = min(second, node.val)
        return -1 if second == float('inf') else second
