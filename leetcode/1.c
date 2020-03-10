#include <stdlib.h>  // for malloc

typedef struct IndexArray {
    int idx;
    int val;
} IndexArray;

int _compare(const void *a, const void *b);

int * twoSum(const int nums[], const int numsSize,
             const int target, int * const returnSize) {
    /* 核心方法 - Combination. */
    const int SIZE = 2;
    int * const res = malloc(SIZE * sizeof(int));

    for (int i = 0; i < numsSize; i ++) {
        for (int j = i + 1; j < numsSize; j ++) {
            if (nums[i] + nums[j] == target) {
                res[0] = i, res[1] = j;
                *returnSize = SIZE;
                return res;
            }
        }
    }

    return res;
}

int * twoSum2(const int nums[], const int numsSize,
              const int target, int * const returnSize) {
    /* 核心方法 - 对撞指针. */
    const int SIZE = 2;
    int l = 0, r = numsSize - 1;
    int * const res = malloc(SIZE * sizeof(int));
    IndexArray array[numsSize];

    for (int i = 0; i < numsSize; i ++) {
        array[i] = (IndexArray) {.idx = i, .val = nums[i]};
    }
    qsort(array, numsSize, sizeof(IndexArray), _compare);

    while (l < r) {
        int sum = array[l].val + array[r].val;
        if (sum == target) {
            res[0] = array[l].idx, res[1] = array[r].idx;
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

int _compare(const void *a, const void *b) {
    const IndexArray *aa = a;
    const IndexArray *bb = b;

    if (aa -> val < bb -> val) {
        return -1;
    } else if (aa -> val > bb -> val) {
        return 1;
    }
    return 0;
}
