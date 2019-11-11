import pytest


class Solution:

    brackets = {
        '{': '}',
        '[': ']',
        '(': ')'
    }

    def isValid(self, s: str) -> bool:
        # empty `s` is valid
        if not s:
            return True

        left = []
        for c in s:
            if c in self.brackets:
                left.append(c)
            # right bracket case, becasue `s` only has bracket
            elif not left or not self.brackets[left.pop()] == c:
                return False

        # left must empty
        return not left


solution = Solution()


@pytest.mark.parametrize(('s', 'result'), (
    ('', True),
    ('{[]}', True),
    ('{{}}[', False),
    ('{{])', False),
    ('}{', False)
))
def test_solution(s: str, result: bool):

    assert solution.isValid(s) == result
