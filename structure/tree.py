from typing import Any, Generator, Iterable, Optional


class BinaryTreeNode:

    def __init__(self, val: Any, left: Optional['BinaryTreeNode'] = None,
                 right: Optional['BinaryTreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

    @classmethod
    def from_list(cls, data: list) -> Optional['BinaryTreeNode']:
        data.insert(0, None)
        return cls._from_list(data, 1)

    @classmethod
    def _from_list(cls, data: list, index: int) -> Optional['BinaryTreeNode']:
        if index >= len(data) or data[index] is None:
            return

        root = cls(data[index])
        root.left = cls._from_list(data, index * 2)
        root.right = cls._from_list(data, index * 2 + 1)
        return root


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

        实际上这种实现可以拓展到中序, 后序等其他实现. 只不过是需要按照
        递归实现中的语句顺序改变 `_operators` 中不同操作的位置.
        """
        def _operators(n: Optional[BinaryTreeNode]) -> list:
            # 空 list 代表没有任何语句.
            if n is None:
                return []
            return [('preorder', n.right),
                    ('preorder', n.left),
                    ('yield', n)]

        if not root:
            return
        nodes = _operators(root)
        while nodes:
            operator, node = nodes.pop()
            if operator == 'yield':
                yield node
            else:
                nodes.extend(_operators(node))

    @classmethod
    def _inorder(cls, root: Optional[BinaryTreeNode]
                 ) -> Optional[Iterable[BinaryTreeNode]]:
        """记录访问节点的次数实现中序遍历.

        中序遍历再第二次访问到节点时才返回.
        """
        if not root:
            return

        nodes = [(0, root)]
        while nodes:
            times, node = nodes.pop()
            if times == 0:
                nodes.extend((t, n) for t, n in ((0, node.right), (1, node), (0, node.left)) if n)
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
