from typing import Any, Generator, Iterable, Optional


class BinaryTreeNode:

    def __init__(self, val: Any,
                 left: Optional['BinaryTreeNode'] = None,
                 right: Optional['BinaryTreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

    @classmethod
    def from_list(cls, data: Iterable) -> Optional['BinaryTreeNode']:
        """根据数组生成一棵树.

        数组和树的对应关系如下图. 树生成数组可以用层序遍历树. 数组生成树可以依照索引,
        索引 0 的子节点: 1, 2, 1 的子节点: 3, 4, 2 的子节点: 5, 6, 类推 n 的
        子节点: (n + 1) * 2 - 1, (n + 1) * 2.

        ```
             1          [1,
          2    3     ->  2, 3,
        4  5  6  7       4, 5, 6, 7]
        ```
        """
        return cls._from_list(tuple(data), 0)

    @classmethod
    def _from_list(cls, data: tuple, index: int) -> Optional['BinaryTreeNode']:
        """根据 `index` 生成节点 (`from_list` 的递归函数)."""
        if index >= len(data) or data[index] is None:
            return

        node = cls(data[index])
        node.left = cls._from_list(data, (index + 1) * 2 - 1)
        node.right = cls._from_list(data, (index + 1) * 2)
        return node


class BinaryTree:
    """迭代实现各种二叉树的操作."""

    @classmethod
    def preorder(cls, root: Optional[BinaryTreeNode]
                 ) -> Optional[Iterable[BinaryTreeNode]]:
        """前序遍历.

        为什么会想到用栈而不是队列呢 ?

        答: 因为栈可以插队, 而队列不行. 当遍历到某个节点时, 必须存储节点的左右节点,
        如果使用队列, 那么无论如何存储, 下两次 `pop` 肯定是这两个节点, 而前序遍历需要
        先遍历左节点的所有子节点再遍历右节点. 使用栈时, 可以右节点先入栈, 左节点再入栈,
        取出左节点, 将左节点的子节点入栈, 这时子节点就插到了右节点的前面, 符合前序遍历.

        如何看待迭代实现和递归实现二者的异同 ?

        答: 实际上二者逻辑类似. 假设每条语句存储到栈中依次执行, 那么最后一条语句
        一定在栈底, `_preorder` 中模拟系统栈实现了前序遍历. 下图展示了 `_preorder`
        运行 `yield root` 和 `preorder root.l` 之后的系统栈. 而对于 `preorder`
        来说没有记录具体的操作, 因而不能准确的对应到递归实现中的语句, 只不过思路类似,
        依然是先入右节点再入左节点.
        ```
        yield root           preorder root.l      yield root.l
        preorder root.l  ->  preorder root.r  ->  preorder root.l.l
        preorder root.r                           preorder root.l.r
                                                  preorder root.r
        ```
        """
        if not root:
            return
        nodes = [root]
        while nodes:
            node = nodes.pop()
            yield node
            nodes.extend(n for n in (node.right, node.left) if n)

    @classmethod
    def inorder(cls, root: Optional[BinaryTreeNode]
                ) -> Generator:
        """中序遍历.

        中序遍历的验证可使用 LeetCode 538.

        跟 `preorder` 比较像的实现参考 `_inorder`, 在前序遍历中第一次遇见
        节点就可以返回, 因此不需要记录访问次数, 中序遍历比前序遍历复杂,
        节点需要第二次遇见才能返回,

        本实现用其他方式简化了存储访问次数. `_left_side` 相当于第一次遇见节点,
        `pop` 相当于第二次遇见节点. TODO 只不过还没想明白是怎么转到这个方法的 ...
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
    def _preorder(cls, root: Optional[BinaryTreeNode]
                  ) -> Optional[Iterable[BinaryTreeNode]]:
        """模拟系统栈实现前序遍历.

        总共有两种操作: 0 代表继续遍历, 1 代表返回节点.

        另外, 只要改变入栈顺序就可以换成中序遍历和后序遍历.
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
    def preorder(cls, root: Optional[BinaryTreeNode]
                 ) -> Optional[Iterable[BinaryTreeNode]]:
        if root is None:
            return

        yield root
        yield from cls.preorder(root.left)
        yield from cls.preorder(root.right)
