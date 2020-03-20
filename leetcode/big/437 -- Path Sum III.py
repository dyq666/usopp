class Solution:
    def pathSum(self, root, sum_):
        self.res = 0
        self._sum(root, sum_)
        return self.res

    def _sum(self, node, sum_):
        if not node:
            return []

        left = self._sum(node.left, sum_)
        right = self._sum(node.right, sum_)
        self.res += left.count(sum_ - node.val)
        self.res += right.count(sum_ - node.val)
        self.res += 1 if sum_ == node.val else 0
        return [v + node.val for v in left] + \
               [v + node.val for v in right] + [node.val]


class Solution02:
    """
    Date: 2018-10-14
    Method: 迭代
    Solution: dfs, 每次计算出的路径都需要 yield 出
    """

    def pathSum(self, root, sum_):
        return sum(paths.count(sum_) for paths in self.iterdfs(root))

    @classmethod
    def iterdfs(cls, node):
        unused = [(node, [])] if node else []
        while unused:
            node, paths = unused.pop()
            new_paths = [path + node.val for path in paths]
            new_paths.append(node.val)
            yield new_paths
            unused.extend(filter(lambda data: data[0],
                                 ((node.left, new_paths), (node.right, new_paths))))
