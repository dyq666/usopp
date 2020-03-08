#include <iso646.h>
#include <stdbool.h>
#include <stdlib.h>  // for NULL, malloc

typedef struct ListNode {
    int val;
    struct ListNode *next;
} ListNode;

ListNode * addTwoNumbers(ListNode *l1, ListNode *l2) {
    /* 核心方法 - LinkedList.

    主链表 (`dummy`) 的停止条件: `l1` 和 `l2` 都走到头, 且没有进位.
    */
    bool has_carry = false;  // 是否有进位.
    ListNode dummy = (ListNode) {.val = -1, .next = NULL};  // -1 代表无效值.
    ListNode *needle = &dummy;

    while (l1 != NULL or l2 != NULL or has_carry) {
        int v1, v2, total;

        v1 = l1 != NULL ? l1 -> val : 0;
        v2 = l2 != NULL ? l2 -> val : 0;
        l1 = l1 != NULL ? l1 -> next : NULL;
        l2 = l2 != NULL ? l2 -> next : NULL;

        total = v1 + v2 + has_carry;
        has_carry = total >= 10;

        needle -> next = malloc(sizeof(ListNode));
        *(needle -> next) = (ListNode) {.val = total % 10, .next = NULL};
        needle = needle -> next;
    }

    return dummy.next;
}
