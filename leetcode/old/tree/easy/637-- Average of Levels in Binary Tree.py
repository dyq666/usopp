from libs.tree import BT

class Solution:
    """
    Date: 2018-10-03
    Method: 迭代
    """
    def averageOfLevels(self, root):
        return [sum(vals) / len(vals) for vals in BT.iterlevel(root)]
