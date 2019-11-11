class Solution(object):
    """
    Date: 2018-10-02
    Method: 递归
    """
    res = None

    def preorder(self, root):
        self.res = []
        self._pre(root)
        return self.res

    def _pre(self, node):
        if not node:
            return

        self.res.append(node.val)
        for child in node.children:
            self._pre(child)


class Solution02(object):
    """
    2018-10-08
    Method: 迭代
    Solution: 使用栈 + 孩子节点右->左入栈
    """
    def preorder(self, root):
        if not root:
            return []

        unused = [root]
        pre = []

        while unused:
            node = unused.pop()
            unused.extend(reversed(node.children))
            pre.append(node.val)

        return pre
