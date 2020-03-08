class Solution:
    """
    Date: 2018-10-07
    Method: 递归
    """
    def isBalanced(self, root):
        self.res = True
        self._depth(root)
        return self.res

    def _depth(self, node):
        if not node:
            return 0

        left = self._depth(node.left)
        right = self._depth(node.right)
        if abs(left - right) > 1:
            self.res = False
        return 1 + max(left, right)


class Solution02:
    """
    Date: 2018-10-24
    Method: 迭代
    Solution: 后序遍历 + dict
    """
    def isBalanced(self, root):
        def left_traversal(n):
            while n:
                if n.right:
                    yield n.right
                yield n
                n = n.left

        depths = {}
        unused = list(left_traversal(root))
        while unused:
            node = unused.pop()
            if unused and node.right is unused[-1]:
                unused.pop()
                unused.append(node)
                unused.extend(left_traversal(node.right))
            else:
                left_depth = depths[node.left] if node.left else 0
                right_depth = depths[node.right] if node.right else 0
                if abs(left_depth - right_depth) > 1:
                    return False
                depths[node] = 1 + max(left_depth, right_depth)

        return True
