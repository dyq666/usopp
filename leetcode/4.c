#include <limits.h>

double findMedianSortedArrays(const int *nums1, const int nums1Size,
                              const int *nums2, const int nums2Size) {
    /* 核心方法 - 有序数组.

    先合并两个有序数组, 在找中位数.
    */
    const int SIZE = nums1Size + nums2Size;
    int nums[SIZE];
    int idx1 = 0, idx2 = 0;

    for (int idx = 0; idx < SIZE; idx ++) {
        int v1 = idx1 < nums1Size ? nums1[idx1] : INT_MAX;
        int v2 = idx2 < nums2Size ? nums2[idx2] : INT_MAX;
        if (v1 < v2) {
            idx1 ++;
        } else {
            idx2 ++;
        }
        nums[idx] = v1 < v2 ? v1 : v2;
    }

    if (SIZE == 0) {
        return 0.0;
    }
    if ((SIZE & 1) == 1) {
        return (double) nums[SIZE / 2];
    } else {
        return (nums[SIZE / 2 - 1] + nums[SIZE / 2]) / 2.0;
    }
}
