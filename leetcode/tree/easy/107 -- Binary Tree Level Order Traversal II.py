from libs.tree import BT

class Solution:
    """
    Date: 2018-10-22
    Method: 递归
    """
    def levelOrderBottom(self, root):
        self.res = []
        self._level(root, 0)
        return self.res[::-1]

    def _level(self, node, level):
        if not node:
            return

        if level == len(self.res):
            self.res.append([])
        self.res[level].append(node.val)

        self._level(node.left, level + 1)
        self._level(node.right, level + 1)

class Solution02:
    """
    Date: 2018-10-10
    Update: 2018-10-11
    Method: 迭代
    """
    def levelOrderBottom(self, root):
        levels = [list(map(lambda n: n.val, level)) for level in BT.iterlevel(root)]
        return levels[::-1]
