class Solution:
    """
    Date: 2018-10-07
    Method: 递归
    Solution: 类似二分查找, 最短共同祖先一定会将两个点分在两边, 并且只有一个点满足.
    """

    def lowestCommonAncestor(self, root, p, q):
        p, q = sorted((p.val, q.val))
        return self._bs(root, p, q)

    def _bs(self, node, min_, max_):
        if not node:
            return

        if min_ <= node.val <= max_:
            return node
        node = node.left if node.val > min_ else node.right
        return self._bs(node, min_, max_)


class Solution02:
    """
    Date: 2018-10-07
    Method: 迭代
    Solution: 类似二分查找
    """

    def lowestCommonAncestor(self, root, p, q):
        if not root:
            return

        p, q = sorted((p.val, q.val))
        while True:
            if p <= root.val <= q:
                return root
            root = root.left if root.val > q else root.right
