class Solution:
    """
    Date: 2018-10-10
    Method: 递归
    """
    def tree2str(self, t):
        if not t:
            return ''

        fmt = '{}({})({})'
        if not t.right and not t.left:
            fmt = '{}{}{}'
        elif not t.right:
            fmt = '{}({}){}'

        return fmt.format(t.val, self.tree2str(t.left), self.tree2str(t.right))


class Solution02:
    """
    Date: 2018-10-10
    Method: 迭代
    """
    def tree2str(self, t):
        if not t:
            return ''

        string = []
        unused = [t]

        while unused:
            node = unused.pop()
            if isinstance(node, str):
                string.append(node)
                continue
            # 按反顺序入栈 -> ({node.val}, node.left, node.right, )
            # 左孩子节点有特殊情况, 就是没有左但是有右的情况需要变成 ()
            left = node.left or (node.right and '()')
            stack = [')', node.right, left, '({}'.format(node.val)]
            unused.extend(filter(None, stack))

        return ''.join(string)[1:-1]
