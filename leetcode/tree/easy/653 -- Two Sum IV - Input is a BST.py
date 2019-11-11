class Solution:
    """
    Date: 2018-10-10
    Method: 迭代
    """
    def findTarget(self, root, k):
        unused = [root] if root else []
        viewed = set()

        while unused:
            node = unused.pop()
            if k - node.val in viewed:
                return True
            else:
                viewed.add(node.val)
            unused.extend(filter(None, (node.left, node.right)))

        return False
