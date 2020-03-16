# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/3 13:33'


class Solution:
    def topKFrequent(self, nums, k):
        """
        直接使用Counter，从源码得知这种方法的O(nlogn)
        """
        from collections import Counter
        counter = Counter(nums)
        return [c[0] for c in counter.most_common(k)]

    def topKFrequent02(self, nums, k):
        """O(nlogk)
        跟队列保存最小频率的区别
        1. 队列最大长度为k
        2. 优先级是freq
        3. 直接返回list不用求差集
        """
        from collections import Counter
        counter = Counter(nums)
        len_counter = len(counter)

        if len_counter == k:
            return list(counter.keys())

        from queue import PriorityQueue as PQ
        # 区别一
        pq, max_len = PQ(), k

        # 区别二
        for num, freq in counter.items():
            if len(pq.queue) < max_len:
                pq.put((freq, num))
            elif freq > pq.queue[0][0]:
                pq.get()
                pq.put((freq, num))

        # 区别3
        return [p[-1] for p in pq.queue]

    def topKFrequent03(self, nums, k):
        """O(nlog(n-k))
        1. 统计频率，k是数，v是频率
        2. 如果k跟总数相同就直接返回所有数
        3. 创建优先队列，计算优先队列的最大长度，遍历所有数，频率。
           这里采取的是存储频率最小的，所以用取反的方式，让队列中频率最大的元素的优先级最小。
           这里如果不好理解的话，只需要把-freq当做优先级。
        4. 如果当前队列长度小于最大长度，直接入队
        5. 如果等于最大长度了，并且当前的优先级(-freq)比队列中优先级最低的元素优先级高(第一个元素)。
           那么把优先级最低的出队列，当前的入队列
        6. 返回所有的数与频率最低的数的差集
        """
        # 步骤一
        from collections import Counter
        counter = Counter(nums)
        len_counter = len(counter)

        # 步骤二
        if len_counter == k:
            return list(counter.keys())

        # 步骤三
        from queue import PriorityQueue as PQ
        pq, max_len = PQ(), len_counter - k

        for num, freq in counter.items():
            # 步骤四
            if len(pq.queue) < max_len:
                pq.put((-freq, num))
            # 步骤5
            elif -freq > pq.queue[0][0]:
                pq.get()
                pq.put((-freq, num))

        # 步骤6
        return list(set(counter.keys()) - set(q[-1] for q in pq.queue))
