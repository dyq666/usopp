class Solution:
    """
    Date: 2018-10-03
    Method: 递归
    Solution: 从 [自身|左|右] 中选择一个(不如思路二)
    """
    def trimBST(self, node, L, R):
        if not node:
            return

        node.left = self.trimBST(node.left, L, R)
        node.right = self.trimBST(node.right, L, R)

        if node.val < L:
            return node.right
        if node.val > R:
            return node.left
        else:
            return node

class Solution02:
    """
    Date: 2018-10-09
    Method: 递归
    Solution: 与解决一思考角度不同, 解决一先保证了左右两边是修整好的, 所以解决一中会遍历所有节点.
    """
    def trimBST(self, root, L, R):
        if not root:
            return
        if root.val < L:
            return self.trimBST(root.right, L, R)
        elif root.val > R:
            return self.trimBST(root.left, L, R)

        root.left = self.trimBST(root.left, L, R)
        root.right = self.trimBST(root.right, L, R)
        return root

class Solution03:
    """
    Date: 2018-10-09
    Method: 递归
    Solution: 只能把合法的子根节点放入栈中
    """

    def trimBST(self, root, L, R):
        root = self._find(root, L, R)
        unused = [root] if root else []
        while unused:
            node = unused.pop()
            node.left = self._find(node.left, L, R)
            node.right = self._find(node.right, L, R)
            unused.extend(filter(None, (node.left, node.right)))
        return root

    def _find(self, node, L, R):
        while node:
            if L <= node.val <= R:
                return node
            node = node.left if node.val > R else node.right
