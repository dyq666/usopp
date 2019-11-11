# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/30 11:15'


class Solution:
    def isHappy(self, n):
        seen = set()
        while True:
            # 步骤一
            if n == 1:
                return True
            # 步骤二
            if n not in seen:
                seen.add(n)
            else:
                return False
            # 步骤三
            n = sum(self._get(n))

    def _get(self, num):
        res = []
        while num:
            res.append((num % 10) ** 2)
            num //= 10
        return res
