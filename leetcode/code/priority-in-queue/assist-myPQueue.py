# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/3 21:07'


import heapq


class MyPriorityQueue:

    def __init__(self):
        self._index = 0
        self.queue = []

    def push(self, priority, val):
        heapq.heappush(self.queue, (priority, self._index, val))
        self._index += 1

    def pop(self):
        return heapq.heappop(self.queue)[-1]


if __name__ == '__main__':
    class A:
        pass

    pq = MyPriorityQueue()
    pq.push(1, A())
    pq.push(1, A())
    print(pq.queue)
