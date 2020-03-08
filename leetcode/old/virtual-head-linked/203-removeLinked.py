# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/1 23:05'


class Solution:
    def removeElements(self, head, val):
        """
        1. 虚拟头入门
        2. 虚拟头创建时一定要连上head
        3. 使用原因是可能从头节点删除节点，如果有虚拟头可以直接用连接操作
        """
        virtual_head = ListNode(None)
        virtual_head.next = head

        link = virtual_head
        needle = head

        while needle:
            # 删除元素link不变, 否则为当前节点
            if needle.val == val:
                link.next = needle.next
            else:
                link = needle
            needle = needle.next

        return virtual_head.next
		
	def removeElements02(self, head, val):
        dummy_head = ListNode(None)
        dummy_head.next = head
        
        pre = dummy_head
        
        while pre.next:
            if pre.next.val == val:
                pre.next = pre.next.next
            else:
                pre = pre.next
                
        return dummy_head.next	
