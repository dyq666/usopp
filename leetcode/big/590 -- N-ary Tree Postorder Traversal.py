class Solution(object):
    """
    Date: 2018-10-02
    """
    res = None

    def postorder(self, root):
        self.res = []
        self._post(root)
        return self.res

    def _post(self, node):
        if not node:
            return

        for child in node.children:
            self._post(child)
        self.res.append(node.val)


class Solution02(object):
    """
    Date: 2018-10-02
    思路: 后序遍历 = 前序遍历从右向左 + 翻转
    """

    def postorder(self, root):
        if not root:
            return []

        res = []
        unused = [root]

        while unused:
            node = unused.pop()
            unused.extend(node.children)
            res.append(node.val)

        return res[::-1]
