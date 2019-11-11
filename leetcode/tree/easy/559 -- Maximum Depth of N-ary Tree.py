class Solution(object):
    """
    Date: 2018-10-02
    思路: 根层 = 1 + 前一层的最大值
    """
    def maxDepth(self, root):
        if not root:
            return 0
        # if in python3
        # return 1 + max((...), defalut=0) 代替下面的代码
        if not root.children:
            return 1

        return 1 + max(self.maxDepth(child) for child in root.children)

class Solution02(object):
    """
    Date: 2018-10-02
    """
    def maxDepth(self, root):
        if not root:
            return 0

        unused = [(root, 1)]
        max_depth = 0

        while unused:
            node, depth = unused.pop()
            unused.extend((child, depth+1) for child in node.children)
            max_depth = max(max_depth, depth)

        return max_depth
