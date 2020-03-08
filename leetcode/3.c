/* TODO LIST
 1. while (*r) 是否等于 while (*r != EOF), 以及是否应该显式的使用 EOF.
 2. 如何初始化数组使所有元素为 0.
 3. chars 代替哈希.
 */

#include <iso646.h>

int lengthOfLongestSubstring(char *s) {
    int chars[128] = {0};
    int max_len = 0;
    char *l = s, *r = s;

    while (*l) {
        if (*r and chars[*r] == 0) {
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
