# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/6/2 16:56'


class Solution:
    def simplifyPath(self, path):
        """
        使用栈的原因：当读到..时需要弹出最近的一个路径
        步骤：
        1. 通过re模块分割字符串
        2. 遍历分割后的字符串，遇到.忽略，遇到..如果栈中有就出栈，没有就算了，剩下的如果是非空的就入栈
        3. 再用'/'进行拼接
        """
        # 步骤一
        import re
        cleaned_path = re.split(r'/+', path)

        # 步骤二
        res = []

        for item in cleaned_path:
            # cleaned_path中可能有被分割出的空字符串
            if item == '.' or item == '':
                continue

            if item == '..':
                if res:
                    res.pop()
            else:
                res.append(item)

        # 步骤三
        return '/' + '/'.join(res)
