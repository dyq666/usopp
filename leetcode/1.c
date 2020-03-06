/**
 * Note: The returned array must be malloced, assume caller calls free().
 */

#include <stdlib.h>

typedef struct {
    int index;
    int value;
} IndexArray;

int _compare(const void *a, const void *b);

int* twoSum(const int nums[], const int numsSize,
            const int target, int * const returnSize) {
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

int* twoSum2(const int nums[], const int numsSize,
             const int target, int * const returnSize) {
    /* 核心方法 - 对撞指针. */
    const int SIZE = 2;
    int l = 0, r = numsSize - 1;
    int *res = malloc(SIZE * sizeof(int));
    IndexArray array[numsSize];

    if (res == NULL) {
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < numsSize; i ++) {
        array[i] = (IndexArray) {.index = i, .value = nums[i]};
    }
    qsort(array, numsSize, sizeof(IndexArray), _compare);

    while (l < r) {
        if (array[l].value + array[r].value == target) {
            res[0] = array[l].index;
            res[1] = array[r].index;
            *returnSize = SIZE;
            return res;
        } else if (array[l].value + array[r].value < target) {
            l ++;
        } else {
            r --;
        }
    }

    return res;
}

int _compare(const void *a, const void *b) {
    const IndexArray *aa = a;
    const IndexArray *bb = b;

    if (aa -> value < bb -> value) {
        return -1;
    } else if (aa -> value > bb -> value) {
        return 1;
    }
    return 0;
}
