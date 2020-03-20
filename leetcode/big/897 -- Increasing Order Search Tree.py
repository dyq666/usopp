# Definition for a binary tree node.
from libs.tree import BT


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    """
    Date: 2018-10-09
    Method: 递归?
    """

    def increasingBST(self, root):
        dummy_head = TreeNode(None)
        needle = dummy_head

        for val in self._in(root):
            needle.right = TreeNode(val)
            needle = needle.right
        return dummy_head.right

    def _in(self, node):
        if not node:
            return  # It is used to stop generator. using `return 1000` also Accepted.

        yield from self._in(node.left)
        yield node.val
        yield from self._in(node.right)


class Solution02:
    """
    Date: 2018-10-09
    Method: 迭代
    Solution: 中序遍历
    """

    def increasingBST(self, root):
        dummy = TreeNode(None)
        needle = dummy
        for node in BT.iterinorder(root):
            needle.right = TreeNode(node.val)
            needle = needle.right
        return dummy.right
