# pylint: disable=redefined-builtin
from libs.tree import BT

class Solution:
    """
    Date: 2018-10-07
    Update: 2018-10-12
    Method: 递归
    Solution: 前序遍历 + 后序
    """
    def hasPathSum(self, root, sum):
        self.cur_sum = 0
        return sum in self.preorder(root)

    def preorder(self, node):
        if not node:
            return

        self.cur_sum += node.val
        if BT.isleaf(node):
            yield self.cur_sum

        yield from self.preorder(node.left)
        yield from self.preorder(node.right)
        self.cur_sum -= node.val

class Solution02:
    """
    Date: 2018-10-24
    Method: 迭代
    Solution: 后序
    """
    def hasPathSum(self, root, sum):
        unused = []
        self.cur_sum = 0
        if self._left_traversal(root, unused, sum) is not None:
            return True

        while unused:
            node = unused.pop()
            if unused and unused[-1] == node.right:
                unused[-1] = node
                if self._left_traversal(node.right, unused, sum) is not None:
                    return True
            else:
                self.cur_sum -= node.val

        return False

    def _left_traversal(self, node, unused, sum):
        while node:
            self.cur_sum += node.val
            if BT.isleaf(node) and self.cur_sum == sum:
                return True

            if node.right:
                unused.append(node.right)
            unused.append(node)
            node = node.left
