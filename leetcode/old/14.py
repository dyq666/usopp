from typing import List

import pytest


class Solution:

    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ''

        i = 0
        for group in zip(*strs):
            if len(set(group)) > 1:
                break
            i += 1

        return strs[0][:i]


solution = Solution()


@pytest.mark.parametrize(('strs', 'result'), (
    ([], ''),
    ([''], ''),
    (['ab', 'b', 'aa'], ''),
    (['aa', 'aac', 'awww'], 'a')
))
def test_solution(strs: List[str], result: str):

    assert solution.longestCommonPrefix(strs) == result
