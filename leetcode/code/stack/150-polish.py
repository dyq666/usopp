# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/2 12:44'


class Solution:
    def evalRPN(self, tokens):
        """
        1. 使用栈的原因：每个操作符需要使用最近的两个数
        2. 需要分清左右数
        3. 需要注意读的是字符
        4. python的除法int(a / b)代替其他语言的a / b, a // b 并不是直接扔掉非0部分(在负数部分，比如-1.8333会变成-2，而在其他语言里是-1)
           如果硬要用，就需要讨论是否为负数而且是否能除尽的问题：(a // b) + 1 if a // b < 0 and a % b != 0 else a // b
        """
        operator = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: (a // b) + 1 if a // b < 0 and a % b != 0 else a // b
        }

        stack = []

        for token in tokens:
            if token in operator:
                # 需要分清左右操作数
                r = stack.pop()
                l = stack.pop()
                stack.append(operator[token](l, r))
            else:
                stack.append(int(token))

        return stack.pop()
