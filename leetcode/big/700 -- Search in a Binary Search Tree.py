class Solution:
    """
    Date: 2018-10-02
    Method: 递归
    Solution: 二分查找
    """

    def searchBST(self, root, val):
        if not root:
            return

        if root.val == val:
            return root
        elif root.val < val:
            return self.searchBST(root.right, val)
        else:
            return self.searchBST(root.left, val)


class Solution02:
    """
    Date: 2018-10-08
    Method: 迭代
    Solution: 二分查找
    """

    def searchBST(self, root, val):
        node = root

        while node:
            if node.val == val:
                return node
            elif node.val > val:
                node = node.left
            else:
                node = node.right
