#include <iso646.h>

int lengthOfLongestSubstring(char *s) {
    /* 核心方法 - Hash.

    这里默认了 `s` 中只有 0-127 的 ASCII code, 因此可以使用 128 长度的
    整数数组完成哈希表的功能, 当字符对应的值为 0 时代表当前字符不在哈希表中,
    反之, 当为 1 时字符在哈希表.
    */
    int chars[128] = {0};
    int max_len = 0;
    char *l = s, *r = s;

    while (*l != '\0') {
        if (*r != '\0' and chars[*r] == 0) {
            chars[*r] = 1;
            r ++;
            max_len = max_len > r - l ? max_len : r - l;
        } else {
            chars[*l] = 0;
            l ++;
        }
    }

    return max_len;
}
