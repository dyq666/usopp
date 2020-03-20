from libs.tree import BT


class Solution:
    """
    Date: 2018-10-21
    Method: 递归
    Solution: 用同一棵树构造出的两棵树走反向进行比较
    """

    def isSymmetric(self, root):
        return self._is_same(root, root)

    def _is_same(self, n1, n2):
        if not all((n1, n2)):  # 不是全有(四选三) + 一个没有(三选一)
            return not any((n1, n2))

        return n1.val == n2.val and self._is_same(n1.left, n2.right) and self._is_same(n1.right, n2.left)


class Solution02:
    """
    Date: 2018-10-10
    Update: 2018-10-11
    Method: 迭代
    Solution: 层序遍历
    """

    def isSymmetric(self, root):
        for level in BT.iterlevel(root, False):
            level = [n.v for n in level]
            mid = len(level) // 2  # [0...mid-1] [mid...-1]
            if level[mid - 1::-1] != level[mid:]:
                return False
        return True
