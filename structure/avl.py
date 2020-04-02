__all__ = (
    'AVL',
)

from typing import Any, Iterable, Iterator, Optional, Tuple

from .tree import BTNode, BTUtil
from .util import not_empty


class AVL:
    """AVL 树."""

    def __init__(self):
        self._size = 0
        self._root: Optional[BTNode] = None

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator:
        """层序遍历."""
        return BTUtil.levelorder(self._root, filter_none=False)

    def add(self, key: Any, value: Any = 0):
        self._root = self._add(self._root, key, value)

    @not_empty
    def remove(self, key: Any):
        """从树中删除键为 `key` 的节点."""
        self._root = self._remove(self._root, key)

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

        self._flush_height(root)
        return self._balance(root)

    def _remove(self, root: BTNode, key: Any) -> Optional[BTNode]:
        """从以 `root` 为根的树中删除键为 `key` 的节点, 返回删除后的树."""
        # `key` 不在树中
        if root is None:
            raise ValueError
        # 找到了删除节点
        if key == root.key:
            if root.right and root.left:
                # _pop_max_from 中保证了 root.left 是平衡的, 但 _pop 之后,
                # root 的平衡性可能变化.
                root.key, root.val, root.left = self._pop_max_from(root.left)
                self._flush_height(root)
                res = self._balance(root)
            else:
                # 这里其实直接把 root 删掉了, 因此不需要维护 root 的平衡性.
                res = root.right or root.left or None
            self._size -= 1
            return res

        if key < root.key:
            root.left = self._remove(root.left, key)
        else:  # key > root.key
            root.right = self._remove(root.right, key)
        self._flush_height(root)
        return self._balance(root)

    @classmethod
    def from_iterable(cls, iterable: Iterable) -> 'AVL':
        avl = cls()
        for key in iterable:
            avl.add(key)
        return avl

    @staticmethod
    def is_avl(node: Optional[BTNode]) -> bool:
        """判断树是否符合 AVL 平衡规则."""
        return all(abs(AVL._get_balance(node) <= 1) for node in BTUtil.preorder(node))

    @staticmethod
    def _right_rotate(root: BTNode):
        """右旋转根节点, 返回旋转之后的节点.

        根挂到左孩子的右边, 左孩子之前的右边挂到根的左边.
        """
        l_child = root.left
        l_child.right, root.left = root, l_child.right
        AVL._flush_height(root)
        AVL._flush_height(l_child)
        return l_child

    @staticmethod
    def _left_rotate(root: BTNode):
        """坐旋转根节点, 返回旋转之后的节点.

        根挂到右孩子的左边, 右孩子之前的左边挂到根的右边.
        """
        r_child = root.right
        r_child.left, root.right = root, r_child.left
        AVL._flush_height(root)
        AVL._flush_height(r_child)
        return r_child

    @staticmethod
    def _flush_height(node: BTNode):
        """更新节点的高度."""
        node.height = 1 + max(AVL._get_height(node.left), AVL._get_height(node.right))

    @staticmethod
    def _get_height(node: Optional[BTNode]) -> int:
        """返回节点的高度, 空节点的高度为 0."""
        if node is None:
            return 0
        return node.height

    @staticmethod
    def _get_balance(node: Optional[BTNode]) -> int:
        """返回节点的平衡因子, 空节点的平衡因子为 0."""
        if node is None:
            return 0
        return AVL._get_height(node.left) - AVL._get_height(node.right)

    @staticmethod
    def _pop_max_from(root: BTNode) -> Tuple[Any, Any, Optional[BTNode]]:
        """删除以 `root` 为根的树中最大节点, 返回最大值和删除之后的树,
        且保证返回的树是平衡的.
        """
        # 找到最大值了
        if root.right is None:
            return root.key, root.val, root.left

        k, v, n = AVL._pop_max_from(root.right)
        root.right = n
        AVL._flush_height(root)
        return k, v, AVL._balance(root)

    @staticmethod
    def _balance(node: BTNode) -> BTNode:
        """
        问: 为什么 AVL 树分成四种需要平衡的情况 ?

        答: 如果一个节点由平衡转为不平衡, 那么一定是左或右子树的某个地方添加了
           一个元素, 此时分成两种需要平衡的情况, 但没有办法在已知的数据下, 将这
           两种情况恢复平衡性, 因此需要继续细分. 左子树添加元素分为左左或左右添
           加了元素, 右子树添加元素分为右左或右右添加了元素, 在这四种情况下都可
           以恢复平衡性, 因此不需要继续细分.

        LL: 初始情况, A 的平衡因子为 2, B 的平衡因子为 1 或 0. 右旋 A 后,
            A 和 B 的高度需要重新计算, 其他元素高度不变, A 的平衡因子为 1 或 0,
            B 的平衡因子为 -1 或 0, 且仍满足 D < B < E < A < C. 所以平衡成功.
        ```
              A(h+2)               B(h+2, h+1)
          B(h+1)  C(h-1)   ->   D(h)  A(h+1, h)
        D(h) E(h, h-1)            E(h, h-1) C(h-1)
        ```

        RR: 初始情况, A 的平衡因子为 -2, C 的平衡因子为 -1 或 0. 左旋 A 后,
            A 和 C 的高度需要重新计算, 其他元素高度不变, A 的平衡因子为 -1 或 0,
            B 的平衡因子为 1 或 0, 且仍满足 B < A < D < C < E. 所以平衡成功.
        ```
              A(h+2)                        C(h+2, h+1)
          B(h-1)  C(h+1)   ->           A(h, h+1)  E(h)
               D(h-1, h) E(h)     B(h-1) D(h-1, h)
        ```

        LR: 初始情况, A 的平衡因子为 2, B 的平衡因子为 -1. 左旋 B 后,
            变为 LL 的情况.
        ```
              A(h+2)                  A(h+2)
          B(h+1)  C(h-1)   ->     E(h+1)  C(h-1)
        D(h-1) E(h)             B(h) G(h-1)
            F(h-1) G(h-1)     D(h-1)F(h-1)
        ```

        RL: 初始情况, A 的平衡因子为 -2, C 的平衡因子为 1. 右旋 C 后,
            变为 RR 的情况.
        ```
              A(h+2)                  A(h+2)
          B(h-1)  C(h+1)   ->     B(h-1)  D(h+1)
               D(h) E(h-1)             F(h-1) C(h)
          F(h-1) G(h-1)                   E(h-1)G(h-1)
        ```
        """
        balance = AVL._get_balance(node)
        # LL
        if balance > 1 and AVL._get_balance(node.left) >= 0:
            return AVL._right_rotate(node)
        # RR
        if balance < -1 and AVL._get_balance(node.right) <= 0:
            return AVL._left_rotate(node)
        # LR
        if balance > 1 and AVL._get_balance(node.left) < 0:
            node.left = AVL._left_rotate(node.left)
            return AVL._right_rotate(node)
        # RL
        if balance < -1 and AVL._get_balance(node.right) > 0:
            node.right = AVL._right_rotate(node.right)
            return AVL._left_rotate(node)

        return node
