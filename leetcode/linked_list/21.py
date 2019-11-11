import pytest

from lib.linked_list import ListNode


class Solution:

    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:

        res_l = ListNode(None)
        dh = res_l

        while l1 and l2:
            if l1.val < l2.val:
                dh.next = l1
                l1 = l1.next
            else:
                dh.next = l2
                l2 = l2.next
            dh = dh.next

        while l1:
            dh.next = l1
            l1 = l1.next
            dh = dh.next

        while l2:
            dh.next = l2
            l2 = l2.next
            dh = dh.next

        return res_l.next


solution = Solution()


@pytest.mark.parametrize('l1, l2, r', (
    ([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),
))
def test_solution(l1: list, l2: list, r: list):
    c = ListNode.from_list


    print(list(iter(solution.mergeTwoLists(c(l1), c(l2)))))

