from libs.tree import BT


class Solution:
    """
    Date: 2018-10-08
    Update: 2018-10-11
    Method: 递归 or 生成器
    """

    def leafSimilar(self, root1, root2):
        return tuple(BT.iterleaves(root1)) == tuple(BT.iterleaves(root2))


class Solution02:
    """
    Date: 2018-10-02
    Update: 2018-10-11
    Method: 迭代
    Solution: dfs
    """

    def leafSimilar(self, root1, root2):
        leaves = lambda root: [node.val for node in BT.iterdfs(root) if BT.isleaf(node)]
        return leaves(root1) == leaves(root2)
