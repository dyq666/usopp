# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/5/31 20:21'


class Solution:
    def reverseBetween(self, head, m, n):
        """
        1. 翻转，并记录相关的值
        2. 拼接
        3. 具体操作都在注释中
        """
        # 当前遍历到的指针和前一个指针
        cur, last = head, None

        # 翻转的开始节点和开始的前一个节点
        left_pre, left = None, head

        # 从第一个节点开始向后到最后一个需要翻转的节点
        for i in range(1, n + 1):

            # 不是从头(m != 1)开始的情况
            if i == m - 1:
                left_pre, left = cur, cur.next
                # 指针后移动
                last = cur
                cur = cur.next
            elif i > m:
                # 翻转指针
                next_ = cur.next
                cur.next = last
                last = cur
                cur = next_
            else:
                # 指针后移动
                last = cur
                cur = cur.next

        """
        翻转的步骤完成, 开始翻转节点与其他节点拼接
        1. 先分为四种情况是否从头翻转，是否翻转到尾
        2. m == 1代表是从头翻转
        3. cur 最后变为None代表是翻转到尾
        4. 所有从头翻转的都返回last，last就是最后一个被翻转的节点
        5. 所有没从头翻转的直接返回头
        6. 所有没从头翻转的可以合二为1，也就是翻转之后接的是cur，如果翻转到尾，cur就是空，所以可以合并
        7. 所有从头翻转的如果是翻转到尾，就让头接None，如果没有就接cur，当翻转到尾时cur is None所以可以合并
        8. 再次就不合并了因为以后可能记不住了
        """

        if m != 1 and cur is not None:
            left.next = cur
            left_pre.next = last
            return head
        elif m == 1 and cur is not None:
            left.next = cur
            return last
        elif m != 1 and cur is None:
            left.next = None  # 跟left.next = cur一样
            left_pre.next = last
            return head
        elif m == 1 and cur is None:
            left.next = None
            return last
