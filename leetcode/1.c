/**
 * Note: The returned array must be malloced, assume caller calls free().
 */

#include <stdlib.h>
#include <string.h>

int _compare_int(const void *a, const void *b);

int* twoSum(const int nums[], int numsSize, int target, int *returnSize) {
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

int* twoSum2(const int nums[], int numsSize, int target, int *returnSize) {
    /* 核心方法 - 对撞指针. */
    const int SIZE = 2;
    int sum, new_nums[numsSize];
    int l = 0, r = numsSize - 1, *res = malloc(SIZE * sizeof(int));

    memcpy(new_nums, nums, numsSize * sizeof(int));

    // TODO 这里需要想办法让 `nums` 的索引参与排序中, 可能需要 struct.
    qsort(new_nums, numsSize, sizeof(int), _compare_int);

    while (l < r) {
        sum = new_nums[l] + new_nums[r];
        if (sum == target) {
            // 初始化 res, -1 作为默认值, 用于判断当前位置是否被修改过.
            for (int i = 0; i < SIZE; i ++) {
                res[i] = -1;
            }
            // res 的每个位置只能被修改一次, 用找到的值去 `nums` 中找到原始的索引.
            for (int i = 0; i < numsSize; i ++) {
                if (res[0] == -1 && nums[i] == new_nums[l]) {
                    res[0] = i;
                } else if (res[1] == - 1 && nums[i] == new_nums[r]) {
                    res[1] = i;
                }
            }
            *returnSize = SIZE;
            return res;
        } else if (sum < target) {
            l ++;
        } else {
            r --;
        }
    }

    return res;
}

int _compare_int(const void *a, const void *b) {
    /* copy from https://devdocs.io/c/algorithm/qsort */
    int value_a = *((const int *) a);
    int value_b = *((const int *) b);

    if (value_a < value_b) {
        return -1;
    } else if (value_a > value_b) {
        return 1;
    }
    return 0;
}
