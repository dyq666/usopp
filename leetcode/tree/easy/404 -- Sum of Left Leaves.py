from libs.tree import BT

class Solution:
    """
    Date: 2018-10-10
    Method: 递归
    Solution: dfs
    """
    def sumOfLeftLeaves(self, root):
        return sum(self._left_leaves(root))

    def _left_leaves(self, node):
        if not node:
            return

        if node.left and BT.isleaf(node.left):
            yield node.left.val
        else:
            yield from self._left_leaves(node.left)
        yield from self._left_leaves(node.right)

class Solution02:
    """
    Date: 2018-10-10
    Method: 递归
    Solution: dfs
    """
    def sumOfLeftLeaves(self, root):
        sum_ = 0
        for node in BT.iterdfs(root):
            if BT.isleaf(node.left):
                sum_ += node.left.val
        return sum_
