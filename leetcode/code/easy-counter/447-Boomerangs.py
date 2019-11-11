# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/30 14:24'


class Solution:
    def numberOfBoomerangs(self, points):
        """
        1. O(n^2)
        2. 以每个点位中心遍历其他点
        """
        from collections import Counter

        len_points = len(points)
        res = 0

        # 遍历每个点
        for i in range(len_points):
            counter = Counter(self._eval_dis(points[i], points[j]) for j in range(len_points) if j != i)
            res += self._eval_sum(counter)

        return res

    def _eval_dis(self, p1, p2):
        """计算两点间的距离，由于只用于比较，不开根号了"""
        return sum((p1[i] - p2[i]) ** 2 for i in range(len(p1)))

    def _eval_sum(self, hash_map):
        """根据每个点对应的不同距离由多少个不同的点计算出总共的个数，比如某个距离是3就能组成3*2情况"""
        return sum([i * (i - 1) for i in hash_map.values() if i >= 2])
