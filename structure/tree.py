from itertools import chain
from typing import Any, Generator, Iterable, Optional


class BinaryTreeNode:
    """二叉树节点."""

    def __init__(self, val: Any,
                 left: Optional['BinaryTreeNode'] = None,
                 right: Optional['BinaryTreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

    @classmethod
    def from_list(cls, data: Iterable) -> Optional['BinaryTreeNode']:
        """根据数组生成一棵树.

        树生成数组可以用层序遍历, 如下图所示:
        ```
             10          [10,
          20   30    ->   20, 30,
        40 50 60 70       40, 50, 60, 70]
        ```

        数组生成树依照索引, 父索引和子节点索引关系:
          - 0: 1, 2
          - 1: 3, 4
          - 2: 5, 6
          - n: (n + 1) * 2 - 1, (n + 1) * 2
        """
        return cls._from_list(tuple(data), 0)

    @classmethod
    def _from_list(cls, data: tuple, index: int) -> Optional['BinaryTreeNode']:
        """根据 `index` 从 `data` 中找到数据, 生成节点 (`from_list` 的递归函数)."""
        if index >= len(data) or data[index] is None:
            return

        node = cls(data[index])
        node.left = cls._from_list(data, (index + 1) * 2 - 1)
        node.right = cls._from_list(data, (index + 1) * 2)
        return node


class BinaryTree:
    """迭代实现各种二叉树的操作."""

    @classmethod
    def preorder(cls, root: Optional[BinaryTreeNode]) -> Generator:
        """前序遍历.

        为什么前序遍历会想到用栈而不是队列呢 ?

        答: 因为栈可以插队, 而队列不行. 当遍历到某个节点时, 必须存储节点的左右节点,
        如果使用队列, 那么无论如何存储, 下两次 `pop` 肯定是这两个节点, 而前序遍历需要
        先遍历左节点的所有子节点再遍历右节点. 使用栈时, 可以右节点先入栈, 左节点再入栈,
        取出左节点, 将左节点的子节点入栈, 这时子节点就插到了右节点的前面, 符合前序遍历.

        如何看待迭代实现和递归实现二者的异同 ?

        答: 实际上二者逻辑类似. 假设每条语句存储到栈中依次执行, 那么最后一条语句
        一定在栈底, `_preorder` 中模拟系统栈实现了前序遍历. 下图展示了 `_preorder`
        运行 `yield root` 和 `preorder root.l` 之后的系统栈 (在 `preorder`
        中, 0 代表操作 preorder, 1 代表操作 yield). `_preorder` 中操作 0 的
        入栈顺序和递归实现中的语句相对应, 递归实现中调换顺序就能实现中序和后序, `_preorder`
        中调换操作 0 的入栈顺序也能实现中序和后序.
        ```
        yield root           preorder root.l      yield root.l
        preorder root.l  ->  preorder root.r  ->  preorder root.l.l
        preorder root.r                           preorder root.l.r
                                                  preorder root.r
        ```

        `preorder` 和 `_preorder` 的区别 ?

        答: `_preorder` 更容易理解, 因为可以和递归实现相对应, 也更容易转换成
        中序和后序. 而 `preorder` 是只针对前序遍历的实现, 减少了入栈出栈的次数,
        因而不能扩展到中序和后序, 当然中序和后序都有自己的优化实现.
        """
        if not root:
            return
        nodes = [root]
        while nodes:
            node = nodes.pop()
            yield node
            nodes.extend(n for n in (node.right, node.left) if n)

    @classmethod
    def inorder(cls, root: Optional[BinaryTreeNode]) -> Generator:
        """中序遍历.

        中序遍历的验证可使用 LeetCode 538.

        TODO 研究为什么要这么做, 怎么从递归转换来的.
        """

        def _left_side(n: BinaryTreeNode) -> Iterable:
            """返回所有左侧的节点 (包括节点本身)."""
            while n:
                yield n
                n = n.left

        if not root:
            return
        nodes = list(_left_side(root))
        while nodes:
            node = nodes.pop()
            yield node
            nodes.extend(_left_side(node.right))

    @classmethod
    def postorder(cls, root: Optional[BinaryTreeNode]) -> Generator:
        """后序遍历.

        TODO 研究为什么要这么做, 怎么从递归转换来的.
        """

        def _left_traversal(n):
            while n:
                if n.right:
                    yield n.right
                yield n
                n = n.left

        unused = list(_left_traversal(root))
        while unused:
            node = unused.pop()
            if unused and node.right is unused[-1]:
                unused[-1] = node
                unused.extend(_left_traversal(node.right))
            else:
                yield node

    @classmethod
    def levelorder(cls, root: Optional[BinaryTreeNode],
                   skip_none: bool = True) -> Generator:
        """层序遍历 (每次都返回一层的节点).

        `skip_none`: 非叶子节点是否返回空子节点.

        层序遍历通常使用队列, 为什么这里用的是 list, list 应该只能用做栈 ?

        答: 虽然这里用的是 list, 但实际上还是先进先出, 只不过这里先进先出的特性是由
        遍历完成的 (先放进 list 的先被访问).
        """
        if not root:
            return
        nodes = [root]

        if skip_none:
            while nodes:
                yield nodes
                nodes = [child for n in nodes
                         for child in (n.left, n.right) if child]
        else:
            while nodes:
                yield nodes
                nodes = (n for n in nodes if n and not cls.isleaf(n))
                nodes = list(chain.from_iterable((n.left, n.right) for n in nodes))

    @classmethod
    def isleaf(cls, node):
        return node and node.left is None and node.right is None

    @classmethod
    def _preorder(cls, root: Optional[BinaryTreeNode]) -> Generator:
        """模拟系统栈实现前序遍历.

        总共有两种操作: 0 代表继续遍历, 1 代表返回节点.

        另外, 只要改变入栈顺序就可以换成中序遍历和后序遍历, 所以用不用这种方式
        再实现其他遍历顺序了.
        """
        if not root:
            return

        nodes = [(0, root)]
        while nodes:
            operator, node = nodes.pop()
            if operator == 0:
                nodes.extend((t, n) for t, n in
                             ((0, node.right), (0, node.left), (1, node)) if n)
            else:
                yield node


class BinaryTreeRecursion:
    """递归实现各种二叉树的操作."""

    @classmethod
    def preorder(cls, root: Optional[BinaryTreeNode]) -> Generator:
        """前序遍历.

        只要改变语句顺序就可以换成中序遍历和后序遍历, 所以就不用这种方式
        再实现其他遍历顺序了.
        """
        if root is None:
            return

        yield root
        yield from cls.preorder(root.left)
        yield from cls.preorder(root.right)
