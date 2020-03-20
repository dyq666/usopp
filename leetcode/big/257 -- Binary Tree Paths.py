from libs.tree import BT


class Solution:
    """
    Date: 2018-10-10
    Method: 递归
    Solution: 前序 + 后序
    """

    def binaryTreePaths(self, root):
        self.cur_path = []
        return list(self.preorder(root))

    def preorder(self, node):
        if not node:
            return

        self.cur_path.append(str(node.val))
        if BT.isleaf(node):
            yield '->'.join(self.cur_path)

        yield from self.preorder(node.left)
        yield from self.preorder(node.right)
        self.cur_path.pop()


class Solution02:
    """
    Date: 2018-10-13
    Update: 2018-10-24
    Method: 迭代
    Solution: 后序
    """

    def binaryTreePaths(self, root):
        self.paths = []
        self.cur_path = []
        unused = list(self._left_traversal(root))

        while unused:
            node = unused.pop()
            if unused and unused[-1] == node.right:
                unused[-1] = node
                unused.extend(self._left_traversal(node.right))
            else:
                self.cur_path.pop()

        return self.paths

    def _left_traversal(self, node):
        while node:
            self.cur_path.append(str(node.val))
            if BT.isleaf(node):
                self.paths.append('->'.join(self.cur_path))

            if node.right:
                yield node.right
            yield node
            node = node.left
