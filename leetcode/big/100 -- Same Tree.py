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
