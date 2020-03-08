class Solution(object):
    """
    Date: 2018-10-09
    Method: 递归
    """
    def levelOrder(self, root):
        self.levels = []
        self._dfs(root, 0)
        return self.levels

    def _dfs(self, node, level):
        if not node:
            return

        levels = self.levels
        if len(levels) == level:
            levels.append([])
        levels[level].append(node.val)

        for child in node.children:
            self._dfs(child, level + 1)

class Solution02(object):
    """
    Date: 2018-10-09
    Method: 迭代
    """
    def levelOrder(self, root):
        level = [root] if root else []
        levels = []

        while level:
            levels.append([node.val for node in level])
            level = [child for node in level for child in node.children]

        return levels
