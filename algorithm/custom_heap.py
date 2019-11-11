"""
AUTHOR: dyq666
DATE: 2018.7.24
1. 最大堆 - MaxHeap
"""

from helper import swap_two_ele, closed_reversed_range, closed_range


class MaxHeap:
    """
    最大堆
    概述
    1. 最大堆有多种实现方式, 这里采用数组的方式实现
       - 最大堆需要满足父亲比两个孩子都大
       - 如果我们按照层序遍历的方式从1开始为节点标号, 那么将有如下公式
       - 公式: 父亲 * 2 = 左, 父亲 * 2 + 1 = 右, 也就是1号节点的左右孩子是2和3号
       - 因此我们采用以1为起始值的数组, 保证数组的索引满足上面的公式即可
    """

    def __init__(self):
        """底层使用list, 但是不使用索引为0的位置, 所以默认情况下数组有一个元素"""
        self.__data = [None]

    def __len__(self):
        """元素个数等于底层数组个数-1, 当然也可以选择维护一个size变量"""
        return len(self.__data) - 1
    
    def __str__(self):
        r"""
        功能: 构建一个三层的树, 使用16进制标识了每个位置对应数组中索引
              67
            /    \        
          23      AB 
         /  \    /  \
        01  45  89  CD
        限制: 只能显示7个数据, 而且每个数据必须是占两位的数字
        1. 获取实例的数据和大小
        2. 先构建一个三层的树, 存放数据, 每层14个元素
        3. 将每行对应数组中的值设置在dict中
        4. 获取每行对应在数组中的数据
        5. 遍历每一层, 将每一层对应的数据写入树中, 注意数组中一个值在树中占两个位置
        6. 将树枝写入
        7. 拼接字符串
        """
        # 1. 获取基本数据
        data = self.__data
        size = len(self)

        # 2. 构建三层树
        trees = []
        for i in range(3):
            trees.append([' ']*14)

        # 3. 构建每层的关系
        tree_map = {
            0: [6, 7],
            1: [2, 3, 10, 11],
            2: [0, 1, 4, 5, 8, 9, 12, 13]
        }

        # 4. 获得每层的数据
        one_values = [data[i] for i in closed_range(1, 1) if i <= size]
        two_values = [data[i] for i in closed_range(2, 3) if i <= size]              
        three_values = [data[i] for i in closed_range(4, 7) if i <= size]              

        # 5. 将每层数据写入
        for level_i, level in enumerate([one_values, two_values, three_values]):
            for i, v in enumerate(level):
                tree_maps = tree_map[level_i]
                trees[level_i][tree_maps[i*2]], trees[level_i][tree_maps[i*2+1]] = str(v)[0], str(v)[1]

        # 6. 写入树枝
        intervals1 = [' '] * 14
        intervals1[4], intervals1[9] = '/', '\\'
        intervals2 = [' '] * 14
        intervals2[1], intervals2[4], intervals2[9], intervals2[12] = '/', '\\', '/', '\\'
        trees.insert(1, intervals1)
        trees.insert(3, intervals2)
        
        # 7. 拼接字符串
        str_tree = '\n'.join(''.join(tree)for tree in trees)
        return str(f'data: {data[1:]}\ntree:\n{str_tree}')

    def heapyfy(self, nums):
        """
        功能: 将一个数组构建为最大堆
        1. 先将所有元素放入data中
        2. heapyfy操作是:
           - 从最后一个父节点开始将每个节点都shift_down
           - 最后一个父节点也就是最后一个子节点的父亲, 而最后一个子节点又存放于我们数组的最后一个值, 因此只需要使用逆向公式 子 // 2 = 父就能得到父的索引
           - 遍历的范围也就是[最后一个父节点, 1], 别忘了1号存储的是我们的根节点, 也就是第一个父节点
        """
        self.__data.extend(nums)

        for i in closed_reversed_range(len(self)//2, 1):
            self.__shift_down(i)

    def insert(self, ele):
        """
        功能: 向堆中增加一个元素
        1. 先将元素加入末尾, 也就是变为最后一个叶子节点
        2. 然后在对最后的叶子节点使用`__shift_up`
        """
        self.__data.append(ele)
        self.__shift_up(len(self))

    def get_max(self):
        """
        功能: 取出最大的元素(堆顶)
        1. 将最后一个元素放入第一个元素的位置, 去除最后一个元素(也就是最大值)
        2. 使用`__shift_down`为第一个元素找到合适的位置
        """
        # 1.
        swap_two_ele(self.__data, 1, len(self))
        max_value = self.__data.pop()

        # 2. 为第一个元素找到合适的位置
        self.__shift_down(1)

        return max_value

    def __shift_up(self, k):
        """
        功能: 为索引k找到适合的位置(将子节点向上走, 找到合适的位置)
        1. 堆节点父亲的索引 = 子索引 // 2
        2. 最后一次的情况是父索引为1
        3. 如果父值小于子值就交换
        """
        while (k > 1 and self.__data[k//2] < self.__data[k]):
            swap_two_ele(self.__data, k//2, k)
            k //= 2

    def __shift_down(self, father):
        """
        功能: 为索引father找到适合的位置(将父节点下移找到合适的位置)
        公式: 子的左index = 父index * 2, 子的右index = 父index * 2 + 1
        1. 只要当前节点还有左节点就继续, 也就是左节点的index要小于等于堆的大小
        2. 找到左右中最大的, 如果有右而且比左大, 则为右, 否则为左
        3. 如果父大于子, 则结束。否则交换父子, 重置父索引。       
        """
        # 1. 还有左节点
        while father * 2 <= len(self):

            # 公式
            l, r = father * 2, father * 2 + 1

            # 2. 找到左右节点中大的内个
            max_child = r if r <= len(self) and self.__data[r] > self.__data[l] else l

            # 3. 如果父大于子, 则结束。否则交换父子, 重置父索引。
            if self.__data[father] > self.__data[max_child]:
                break
            else:
                swap_two_ele(self.__data, father, max_child)
                father = max_child


if __name__ == '__main__':
    from random import randint

    # 构建一个最大堆
    max_heap = MaxHeap()
    max_heap.heapyfy(randint(10, 99) for _ in range(7))

    # 输出一开始的树
    print(max_heap)

    # 逐渐取出所有最大值
    while max_heap:
        max_heap.get_max()
        print(max_heap)
