#include <stdbool.h>
#include <stdlib.h>

typedef struct ListNode {
    int val;
    struct ListNode *next;
} ListNode;

ListNode * addTwoNumbers(ListNode *l1, ListNode *l2) {
    /* 核心方法 - 链表.

    主链表 (`dummy`) 的停止条件: `l1` 和 `l2` 都走到头, 且没有进位.
    */
    int v1, v2, total;

    bool has_carry = false;  // 是否有进位.
    ListNode dummy = (ListNode) {.val = -1, .next = NULL};
    ListNode *needle = &dummy;

    while (l1 || l2 || has_carry) {
        v1 = l1 == NULL ? 0 : l1 -> val;
        v2 = l2 == NULL ? 0 : l2 -> val;
        // TODO 为什么不能用 `l1 = l1 && l1 -> next;` ?
        l1 = l1 == NULL ? l1 : l1 -> next;
        l2 = l2 == NULL ? l2 : l2 -> next;

        total = v1 + v2 + has_carry;
        has_carry = total >= 10;

        needle -> next = malloc(sizeof(ListNode));
        *(needle -> next) = (ListNode) {.val = total % 10, .next = NULL};
        needle = needle -> next;
    }

    return dummy.next;
}
