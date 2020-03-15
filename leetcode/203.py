from .util import ListNode


class Solution:
    """核心方法 - 链表.

    是一道非常典型的链表问题, 既要考虑头尾的问题, 又要处理 `prev`, `cur`
    两个指针移动的问题. 本题必须确保所有元素都被 `cur` 指针指向过, 而删除一个
    元素又需要 `cur` 指针的前一个元素, 即 `prev` 指针. 假设本次没有删除元素,
    则 `prev` 向前移动一位, 删除了则不移动.
    """

    @staticmethod
    def removeElements(head: ListNode, val: int) -> ListNode:
        # 删除第一个元素和其他元素逻辑不同, 因此引入 dummy_head, 使第一个元素也有 `prev`.
        dummy = ListNode(None)
        dummy.next = head

        prev = dummy
        cur = dummy.next

        while cur is not None:
            if cur.val == val:
                prev.next = cur.next
                cur.next = None
            else:
                prev = prev.next
            cur = prev.next

        return dummy.next

    @staticmethod
    def removeElements2(head: ListNode, val: int) -> ListNode:
        # 删除第一个元素和其他元素逻辑不同, 因此引入 dummy_head, 使第一个元素也有 `prev`.
        dummy = ListNode(None)
        dummy.next = head

        prev = dummy

        while prev.next is not None:
            if prev.next.val == val:
                cur = prev.next
                prev.next = cur.next
                cur.next = None
            else:
                prev = prev.next

        return dummy.next


if __name__ == '__main__':
    """
    1. 头结点, 尾结点, 中间结点都有目标值.
    2. 删除空节点.
    3. 连续两个目标节点, 主要是测试 `prev` 移动是否正确.
    """
    val = 1
    fs = [Solution.removeElements, Solution.removeElements2]

    for f in fs:
        # 1
        node = ListNode.from_iterable([1, 2, 3, 1, 4, 1])
        assert list(f(node, val)) == [2, 3, 4]

        # 2
        assert f(None, 1) is None

        node = ListNode.from_iterable([1, 1])
        assert f(node, val) is None
