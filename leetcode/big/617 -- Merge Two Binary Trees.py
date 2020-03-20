class Solution:
    """
    Date: 2018-10-02
    Method: 递归
    Solution: 两棵树相应位置的节点都存在时, 执行合并.
              其余情况终止递归.
    """

    def mergeTrees(self, t1, t2):
        if not (t1 and t2):
            return t1 or t2

        t1.val += t2.val
        t1.left = self.mergeTrees(t1.left, t2.left)
        t1.right = self.mergeTrees(t1.right, t2.right)
        return t1


class Solution02:
    """
    Date: 2018-10-07
    Method: 迭代
    Solution: 两棵树相应位置的节点都存在时, 执行合并.
              处理子节点时有三种情况, 都存在则放入栈之后处理, 其余三种情况只用解决 n1 的子节点不存在的情况.
              因为 n2 不存在不影响 n1, n1 n2 都不存在可以融合到 n1 不存在的情况.
    """

    def mergeTrees(self, t1, t2):
        if not (t1 and t2):
            return t1 or t2

        stack = [(t1, t2)]
        while stack:
            n1, n2 = stack.pop()
            if n1 and n2:
                n1.val += n2.val
            self._resolve_child(n1, n2, stack, 'left')
            self._resolve_child(n1, n2, stack, 'right')

        return t1

    def _resolve_child(self, node1, node2, stack, direction):
        child1, child2 = getattr(node1, direction), getattr(node2, direction)
        if not child1:
            setattr(node1, direction, child2)
        elif child1 and child2:
            stack.append((child1, child2))
