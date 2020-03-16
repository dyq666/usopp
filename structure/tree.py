from typing import Any, Iterable, Optional


class BinaryTreeNode:

    def __init__(self, val: Any, left: Optional['BinaryTreeNode'] = None,
                 right: Optional['BinaryTreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


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
        一定在栈底, 再将递归实现的语句缩成最后两句, 我们可以得到以下示意结果. 初始栈
        中有 preorder(左节点), preored(右节点) 两条语句, 当执行到 preorder(左节点)
        时, 需要将此函数的语句 (preorder(左节点.左节点) preorder(左节点.右节点)) 入栈.
        因此迭代的实现其实是在模拟一个系统栈运行函数.

        ```
        yf preorder(root.l)  -> yf preorder(root.l.l)
        yf preorder(root.r)     yf preorder(root.l.r)
                                yf preorder(root.r)
        ```
        """
        if not root:
            return
        nodes = [root]
        while nodes:
            node = nodes.pop()
            yield node
            nodes.extend(n for n in (node.right, node.left) if n)


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
