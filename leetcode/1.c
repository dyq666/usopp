/**
 * Note: The returned array must be malloced, assume caller calls free().
 */

#include <stdlib.h>

int* twoSum(const int* nums, int numsSize, int target, int* returnSize) {
    /* 核心方法 - Combination. */
    const int SIZE = 2;
    int *res = malloc(SIZE * sizeof(int));

    if (res == NULL) {
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < numsSize; i ++) {
        for (int j = i + 1; j < numsSize; j ++) {
            if (nums[i] + nums[j] == target) {
                res[0] = i;
                res[1] = j;
                *returnSize = SIZE;
                return res;
            }
        }
    }

    return res;
}
