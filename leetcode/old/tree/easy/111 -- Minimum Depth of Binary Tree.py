from libs.tree import BT

class Solution:
    """
    Date: 2018-10-10
    Method: 递归
    Solution: 需要求最小值, 所以用无穷大标志没有值
    """
    def minDepth(self, root):
        if not root:
            return 0

        # 都没有返回 0, 有一个返回这个, 都有返回最小的
        left = self.minDepth(root.left) or float('inf')
        right = self.minDepth(root.right) or float('inf')
        return 1 + (0 if left == right == float('inf') else min(left, right))

class Solution02:
    """
    Date: 2018-10-13
    Method: 迭代
    Solution: dfs 存储: (node, depth) 或者层序遍历到有叶子节点的层
    """
    def minDepth(self, root):
        if not root:
            return 0

        depth = 0
        for level in BT.iterlevel(root):
            depth += 1
            for node in level:
                if BT.isleaf(node):
                    return depth
