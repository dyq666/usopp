class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    """
    Date: 2018-10-10
    Method: 递归
    """
    def sortedArrayToBST(self, nums):
        if not nums:
            return

        mid = len(nums) // 2

        node = TreeNode(nums[mid])
        node.left = self.sortedArrayToBST(nums[:mid])
        node.right = self.sortedArrayToBST(nums[mid+1:])
        return node

class Solution02:
    """
    Date: 2018-10-23
    Method: 迭代
    Solution: 使用 dict 记录每个遍历过的节点, 栈中记录每个节点的左右范围和父亲的索引.
    """
    def sortedArrayToBST(self, nums):
        if not nums:
            return []

        n = len(nums)
        nodes = {}
        unused = [(0, n - 1, -1)]  # left, right, father_index
        while unused:
            l, r, father = unused.pop()
            mid = (l + r) // 2
            nodes[mid] = TreeNode(nums[mid])
            self._concat(nodes, father, mid)
            unused.extend(self._children(mid, l, r))
        return nodes[(0 + n - 1) // 2]

    def _children(self, i, l, r):
        if l <= i - 1:
            yield (l, i - 1, i)
        if i + 1 <= r:
            yield (i + 1, r, i)

    def _concat(self, nodes, father, child):
        if father in nodes:
            direction = 'left' if child < father else 'right'
            setattr(nodes[father], direction, nodes[child])
