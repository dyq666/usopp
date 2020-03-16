# _*_ coding: utf-8 _*_
__author__ = "dyq666"
__date__ = "2018/5/25 19:18"


class Solution:
    def fourSumCount(self, A, B, C, D):
        """
        1. O(n^3)
        2. 采用之前的思路
        3. 将AB看成是外层的两层循环
        4. 将CD看成是内层, 将其中之一做成dict, 另一个则遍历去寻找
        """
        res_num = 0

        # 将C/D其中一个转为dict, 并且记录每个值有几个
        c_dict = {}
        for c in C:
            c_dict[c] = c_dict.setdefault(c, 0) + 1

        for a in A:
            for b in B:

                # 由于存储的是C所以遍历D
                for d in D:

                    search = 0 - a - b - d
                    if search in c_dict:
                        res_num += c_dict[search]

        return res_num

    def fourSumCount02(self, A, B, C, D):
        """
        1. O(n^2)
        2. 特殊情况, 这里给的是四个数组而不是一个数组, 将四个数组分成两部分处理,
           分成两部分处理保证了每部分都是两个for
        3. 分成两部分后又回到了2Sum中使用Hash的问题, 需要注意的是不能使用set,
           因为一个和可能由不同的值相加得到, 需要使用dict来存储频率
        """
        res_num = 0

        target_dict = {}
        for a in A:
            for b in B:
                target_dict[a+b] = target_dict.setdefault(a+b, 0) + 1

        for d in D:
            for c in C:
                if -(c + d) in target_dict:
                    res_num += target_dict[-(c + d)]

        return res_num

    def fourSumCount03(self, A, B, C, D):
        """
        1. O(n^2)
        2. 优化02中的代码, 使代码更加pythonic
        3. 将02中的代码拆分两步骤
        4. 步骤一, 统计频率
        5. 步骤二, 计算每个值对应的个数, 然后求和
        """
        import collections

        target_dict = collections.Counter(a+b for a in A
                                              for b in B)

        return sum(target_dict[-(c + d)] for c in C
                                         for d in D
                                         if -(c + d) in target_dict)


if __name__ == '__main__':
    A = [0, 1, -1]
    B = [-1, 1, 0]
    C = [0, 0, 1]
    D = [-1, 1, 1]
    solution = Solution()
    print(solution.fourSumCount03(A, B, C, D))
