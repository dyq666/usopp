import pytest


class Solution:

    def simplifyPath(self, path: str) -> str:
        r = []
        for i in path.split('/'):
            if i == '' or i == '.':
                continue

            if i != '..':
                r.append(i)
            elif r:  # c == '..' and r
                r.pop()

        return '/' + '/'.join(r)


solution = Solution()


@pytest.mark.parametrize(('path', 'result'), (
    ('', '/'),
    ('/a//b/', '/a/b'),
    ('/a///b/././.', '/a/b'),
    ('../a/', '/a'),
    ('../a/../', '/')
))
def test_solution(path: str, result: str):
    assert solution.simplifyPath(path) == result
