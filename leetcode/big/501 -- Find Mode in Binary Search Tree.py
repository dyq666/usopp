from libs.tree import BT


class Solution:
    """
    Date: 2018-10-25
    Method: 迭代
    Solution: dfs
    """

    def findMode(self, root):
        if not root:
            return []
        from collections import Counter
        counter = Counter(node.val for node in BT.iterdfs(root))
        max_ = counter.most_common(1)[0][1]
        return [k for k, v in counter.items() if v == max_]
