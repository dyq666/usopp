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
    """AVL 树."""
