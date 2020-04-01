__all__ = (
    'AVL',
)

from typing import Any, Iterable, Iterator, Optional

from .tree import BTNode, BTUtil


class AVL:
    """AVL 树.

    问: 为什么 AVL 树分成四种需要平衡的情况 ?

    答: 如果一个节点由平衡转为不平衡, 那么一定是左或右子树的某个地方添加了
       一个元素, 此时分成两种需要平衡的情况, 但没有办法在已知的数据下, 将这
       两种情况恢复平衡性, 因此需要继续细分. 左子树添加元素分为左左或左右添
       加了元素, 右子树添加元素分为右左或右右添加了元素, 在这四种情况下都可
       以恢复平衡性, 因此不需要继续细分.

    TODO 一个遗留的疑问, 在 LL 时, 我并没有找到根平衡因子为 2, 但左孩子平衡
         因子为 0 的情况. 同理, 在 RR 时, 我也没有找到根平衡因子为 2, 但右
         孩子平衡因子为 0 的情况. LR, RR 也一样.

    LL: 初始情况, 根的平衡因子为 1, 左孩子的平衡因子为 0. 添加元素之后,
        根的平衡因子为 2, 左孩子的平衡因子为 1. 右旋后 (根挂到左孩子的右边,
        左孩子的右边挂到根的左边), 由于根节点下降了两层, 高度从 h+3 -> h+1.
        其他节点高度不变, 使得根和右孩子的平衡因子都变为 0. 而且依然满足二叉
        搜索树的特性, 因此平衡成功.
    ```
          A(h+2)                 A(h+3)                 B(h+2)
      B(h+1)  C(h)    ->      B(h+2)  C(h)    ->   D(h+1)  A(h+1)
    D(h) E(h)              D(h+1) E(h)                  E(h)  C(h)
    ```

     RR: 初始情况, 根的平衡因子为 -1, 右孩子的平衡因子为 0. 添加元素之后,
         根的平衡因子为 -2, 右孩子的平衡因子为 -1. 左旋后 (根挂到右孩子的左边,
         右孩子的左边挂到根的右边), 由于根节点下降了两层, 高度从 h+3 -> h+1.
         其他节点高度不变, 使得根和右孩子的平衡因子都变为 0. 而且依然满足二叉
         搜索树的特性, 因此平衡成功.
    ```
          A(h+2)                A(h+3)                 C(h+2)
      B(h)  C(h+1)    ->    B(h)  C(h+2)    ->      A(h+1)  E(h+1)
          D(h) E(h)             D(h) E(h+1)      B(h) D(h)
    ```

    LR: 初始情况, 根的平衡因子为 1, 左孩子的平衡因子为 0. 添加元素之后,
        根的平衡因子为 2, 左孩子的平衡因子为 -1. 先让左孩子左旋转, 然后
        变成了 LL 的情况, 按照 LL 进行处理即可.
    ```
            A(h+2)               A(h+3)              A(h+3)
        B(h+1)  C(h)    ->    B(h+2)  C(h)   ->   E(h+2)  C(h)
     D(h)  E(h)            D(h) E(h+1)          B(h+1)
                                              D(h)
    ```

    RL: 初始情况, 根的平衡因子为 -1, 右孩子的平衡因子为 0, 添加元素之后,
        根的平衡因子为 -2, 右孩子的平衡因子为 -1. 先让右孩子右旋转, 然后
        变成了 RR 的情况, 按照 RR 进行处理节课.
    ```
            A(h+2)               A(h+3)              A(h+3)
        B(h)  C(h+1)    ->    B(h)  C(h+2)   ->   B(h)  D(h+2)
           D(h)  E(h)              D(h+1) E(h)            C(h+1)
                                                             E(h)
    ```
    """

    def __init__(self):
        self._size = 0
        self._root: Optional[BTNode] = None

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator:
        """层序遍历."""
        return BTUtil.levelorder(self._root)

    def add(self, key: Any, value: Any = 0):
        self._root = self._add(self._root, key, value)

    def _add(self, root: Optional[BTNode], key: Any, value: Any = 0):
        """在以 `root` 为根的树中添加节点, 返回添加完成后的树."""
        if root is None:
            self._size += 1
            return BTNode(key, value, height=1)

        # 相等时更新值
        if key == root.key:
            root.val = value
        elif key < root.key:
            root.left = self._add(root.left, key, value)
        else:
            root.right = self._add(root.right, key, value)

        self.flush_height(root)

        balance = self.get_balance(root)
        # LL
        if balance > 1 and self.get_balance(root.left) > 0:
            return self._right_rotate(root)
        # RR
        if balance < -1 and self.get_balance(root.right) < 0:
            return self._left_rotate(root)
        # LR
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)
        # RL
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)

        return root

    @classmethod
    def from_iterable(cls, iterable: Iterable) -> 'AVL':
        avl = cls()
        for key in iterable:
            avl.add(key)
        return avl

    @staticmethod
    def _right_rotate(root: BTNode):
        """右旋转根节点, 返回旋转之后的节点.

        根挂到左孩子的右边, 左孩子之前的右边挂到根的左边.
        """
        l_child = root.left
        l_child.right, root.left = root, l_child.right
        AVL.flush_height(l_child)
        AVL.flush_height(root)
        return l_child

    @staticmethod
    def _left_rotate(root: BTNode):
        """坐旋转根节点, 返回旋转之后的节点.

        根挂到右孩子的左边, 右孩子之前的左边挂到根的右边.
        """
        r_child = root.right
        r_child.left, root.right = root, r_child.left
        AVL.flush_height(r_child)
        AVL.flush_height(root)
        return r_child

    @staticmethod
    def flush_height(node: BTNode):
        """更新节点的高度."""
        node.height = 1 + max(AVL.get_height(node.left), AVL.get_height(node.right))

    @staticmethod
    def get_height(node: Optional[BTNode]) -> int:
        """返回节点的高度, 空节点的高度为 0."""
        if node is None:
            return 0
        return node.height

    @staticmethod
    def get_balance(node: Optional[BTNode]) -> int:
        """返回节点的平衡因子, 空节点的平衡因子为 0."""
        if node is None:
            return 0
        return AVL.get_height(node.left) - AVL.get_height(node.right)

    @staticmethod
    def is_avl(node: Optional[BTNode]) -> bool:
        """判断树是否符合 AVL 平衡规则."""
        gen = (False for node in BTUtil.preorder(node) if abs(AVL.get_balance(node) > 1))
        return next(gen, True)
