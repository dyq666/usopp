__all__ = (
    'AVL',
)

from typing import Any, Optional


class Node:
    """AVL 树节点.

    由于可以用 AVL 树实现字典, 因此节点中记录了 k/v.
    如果用于实现集合, 那么只使用 k 即可 (val 默认为 0).
    """

    def __init__(self, key: Any, val: Any = 0,
                 height: int = 1,
                 left: Optional['Node'] = None,
                 right: Optional['Node'] = None):
        self.key = key
        self.val = val
        self.height = height
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__}'
            f' key={self.key!r}'
            f' val={self.val!r}'
            f' height={self.height!r}'
            f'>'
        )


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
         孩子平衡因子为 0 的情况.

    LL: 初始情况, 根的平衡因子为 1, 左孩子的平衡因子为 0. 添加元素之后,
        根的平衡因子为 2, 左孩子的平衡因子为 1. 右旋后 (根挂到左孩子的右边,
        左孩子的右边挂到根的左边), 由于根节点下降了两层, 高度从 h+3 -> h+1.
        其他节点高度不变, 使得根和右孩子的平衡因子都变为 0. 而且依然满足二叉
        搜索树的特性, 因此平衡成功.
    ```
        h+2             h+3            h+2
      h+1  h    ->    h+2  h    ->   h+1  h+1
     h  h           h+1 h                h  h
    ```

     RR: 初始情况, 根的平衡因子为 -1, 右孩子的平衡因子为 0. 添加元素之后,
         根的平衡因子为 -2, 右孩子的平衡因子为 -1. 左旋后 (根挂到右孩子的左边,
         右孩子的左边挂到根的右边), 由于根节点下降了两层, 高度从 h+3 -> h+1.
         其他节点高度不变, 使得根和右孩子的平衡因子都变为 0. 而且依然满足二叉
         搜索树的特性, 因此平衡成功.
    ```
        h+2             h+3            h+2
      h  h+1    ->    h  h+2    ->   h+1  h+1
        h  h            h h+1       h  h
    ```
    """
