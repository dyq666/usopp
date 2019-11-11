from itertools import zip_longest

from libs.tree import BT

class Solution:
    """
    Date: 2018-10-04
    Update: 2018-10-11
    Method: 递归
    Note:
          1 1 all()     a
          0 1           ny  not
          1 0           ()  all
          0 0 not any()      ()
    """
    def isSameTree(self, p, q):
        if not all((p, q)):  # 不是全有(四选三) + 一个没有(三选一)
            return not any((p, q))

        return p.val == q.val and self.isSameTree(p.left, q.left) \
                                and self.isSameTree(p.right, q.right)

class Solution02:
    """
    Date: 2018-10-10
    Update: 2018-10-21
    Method: 迭代
    Solution: 同时 dfs(含 None) 两棵树.
    """
    def isSameTree(self, p, q):
        for n1, n2 in zip_longest(BT.iterdfs(p, False), BT.iterdfs(q, False)):
            v1 = n1 and n1.val
            v2 = n2 and n2.val
            if v1 != v2:
                return False
        return True
