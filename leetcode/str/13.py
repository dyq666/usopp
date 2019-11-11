class Solution:

    roman = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000,
    }

    def romanToInt(self, s: str) -> int:
        if not s:
            return 0

        res = 0
        # traverse [0, n-2]
        for cur, next in zip(s[:-1], s[1:]):
            cur, next = self.roman[cur], self.roman[next]
            res += cur if cur >= next else -cur

        # add last one
        return res + self.roman[s[-1]]
