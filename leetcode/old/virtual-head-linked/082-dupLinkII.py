# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/1 23:58'


class Solution:
    def deleteDuplicates(self, head):
        """
        1. 创建头指针，可能会删除头指针的节点
        2. link_move的作用是需要看两个节点才能确定一个节点将不会被删去，也就才能将link移至该节点
           之后link_move就不会再等于0了，因为第一个节点的两个不重复节点相当于第二个节点的一个不重复节点
        3. last节点记录着link节点如果可以移动，要移动到哪个节点上，如果是被删除的节点，last将回到link的位置
        """
        virtual_head = ListNode(None)
        virtual_head.next = head

        duplicate_val = None
        link_move = 0

        needle = head
        last = None
        link = virtual_head

        while needle:
            next_ = needle.next

            if needle.val != duplicate_val:
                duplicate_val = needle.val
                link_move += 1

                # 移动link节点
                if link_move == 2:
                    link = last
                    link_move = 1
                last = needle
            else:
                link.next = needle.next
                last = link

            needle = next_

        return virtual_head.next
