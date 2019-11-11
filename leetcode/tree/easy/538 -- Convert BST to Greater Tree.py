from libs.tree import BT

class Solution:
    """
    Date: 2018-10-04
    Method: 递归
    Solution: 中序遍历从右走
    """
    def convertBST(self, root):
        self.sum_ = 0
        self._inorder(root)
        return root

    def _inorder(self, node):
        if not node:
            return

        self._inorder(node.right)
        node.val += self.sum_
        self.sum_ = node.val
        self._inorder(node.left)

class Solution02:
    """
    Date: 2018-10-10
    Method: 迭代
    Solution: 中序遍历从右走
    """
    def convertBST(self, root):
        sum_ = 0
        for node in BT.iterinorder(root, 'right'):
            node.val += sum_
            sum_ = node.val
        return root
