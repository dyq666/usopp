__all__ = (
    'BST', 'BSTDict', 'BTNode', 'BTUtil'
)

from itertools import chain, zip_longest
from typing import Any, Generator, List, Iterable, Iterator, Optional, Tuple

from .util import no_value, not_empty


class BTNode:
    """二叉树节点.

    由于可以用二分搜索树实现字典, 因此节点中记录了 k/v.
    如果用于实现集合, 那么只使用 k 即可 (val 默认为 0).

    由于 AVL 树中需要记录高度, 因此增加了 `height` 属性.
    """

    def __init__(self, key: Any, val: Any = 0,
                 height: int = 1,
                 left: Optional['BTNode'] = None,
                 right: Optional['BTNode'] = None):
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


class BTUtil:
    """二叉树常用操作."""

    @staticmethod
    def preorder(root: Optional[BTNode]) -> Generator[BTNode, None, None]:
        if root is None:
            return

        nodes = [root]
        while nodes:
            node = nodes.pop()
            yield node
            # 先遍历左后遍历右, 因此右先入栈.
            nodes.extend(child for child in (node.right, node.left) if child)

    @staticmethod
    def preorder_with_mocked_stack(root: Optional[BTNode]
                                   ) -> Generator[BTNode, None, None]:
        """模拟系统栈实现前序遍历.

        改变入栈顺序就可以换成中序和后序.

        `preorder_with_mocked_stack` 和 `preorder_with_recursion` 的关系 ?

        答: 二者实际都是递归的实现, 只不过前者是模拟后者的系统栈调用. 具体语句的对应关系
           在注释中写明了.

        `preorder` 和 `preorder_with_mocked_stack` 的区别 ?

        答: `preorder_with_mocked_stack` 更容易理解, 更容易转换成中序和后序遍历.
           而 `preorder` 是前序遍历的标准实现, 不能扩展到中序和后序, 当然, 中序和后序
           都有自己的标准实现.
        """
        if root is None:
            return

        # (操作码, 节点), 操作码有 0, 1 两种, 其中 0 代表执行前序遍历, 1 代表返回节点.
        statements = [(0, root)]
        while statements:
            operator, node = statements.pop()
            # 等价于执行一次 `preorder_with_recursion`
            if operator == 0:
                # 等价于 `preorder_with_recursion` 中的递归终止条件.
                if node is None:
                    continue
                # 等价于将 `preorder_with_recursion` 中的三条语句入栈.
                statements.extend(((0, node.right),
                                   (0, node.left),
                                   (1, node)))
            else:
                yield node

    @staticmethod
    def preorder_with_recursion(root: Optional[BTNode]
                                ) -> Generator[BTNode, None, None]:
        """递归实现前序遍历.

        改变语句顺序就可以换成中序和后序.
        """
        if root is None:
            return

        yield root
        yield from BTUtil.preorder_with_recursion(root.left)
        yield from BTUtil.preorder_with_recursion(root.right)

    @staticmethod
    def inorder(root: Optional[BTNode]) -> Generator[BTNode, None, None]:
        """中序遍历.

        中序遍历可在 LeetCode 538 中测试.

        这是一个标准版的非递归实现.
        """

        def _left_side(n: BTNode) -> Iterable:
            """返回所有左侧的节点 (包括节点本身)."""
            while n:
                yield n
                n = n.left

        if root is None:
            return

        nodes = list(_left_side(root))
        while nodes:
            node = nodes.pop()
            yield node
            nodes.extend(_left_side(node.right))

    @staticmethod
    def postorder(root: Optional[BTNode]) -> Generator[BTNode, None, None]:
        """后序遍历.

        这是一个标准版的非递归实现.
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

    @staticmethod
    def levelorder_with_level(root: Optional[BTNode], filter_none: bool = True
                              ) -> Generator[List[Optional[BTNode]], None, None]:
        """层序遍历 (每次都返回一层的节点).

        `filter_none`: 是否过滤空子节点.

        层序遍历通常使用队列, 为什么这里用的是 list, list 应该只能用做栈 ?

        答: 虽然这里用的是 list, 但实际上还是先进先出, 只不过这里先进先出的特性是由
           遍历完成的 (先放进 list 的先被访问).
        """
        if root is None:
            return

        level = [root]
        while level:
            yield level
            if filter_none:
                # 所有 node 都不可能为空
                level = [child for n in level
                         for child in (n.left, n.right) if child]
            else:
                # node 可能为空
                gen = ((n.left, n.right) for n in level if n and not BTUtil.isleaf(n))
                level = list(chain.from_iterable(gen))

    @staticmethod
    def levelorder(root: Optional[BTNode], filter_none: bool = True
                   ) -> Generator[Optional[BTNode], None, None]:
        """层序遍历 (每次只返回一个节点)."""
        return (n and n.key
                for level in BTUtil.levelorder_with_level(root, filter_none=filter_none)
                for n in level)

    @staticmethod
    def is_equal(one: Optional[BTNode], other: Optional[BTNode]) -> bool:
        """判断两棵树是否相同.

        这里可用任意遍历方式, 但无论哪种都必须返回空子节点.

        此外, 可以在 LeetCode 100 中测试.
        """
        for level1, level2 in zip_longest(BTUtil.levelorder_with_level(one, filter_none=False),
                                          BTUtil.levelorder_with_level(other, filter_none=False),
                                          fillvalue=[]):
            v1 = [n and n.key for n in level1]
            v2 = [n and n.key for n in level2]
            if v1 != v2:
                return False
        return True

    @staticmethod
    def isleaf(node: Optional[BTNode]) -> bool:
        return bool(node and node.left is None and node.right is None)

    @staticmethod
    def left_idx(index: int) -> int:
        """返回 `index` 的左孩子索引.

        如何推导出父索引和孩子索引之间的关系 ?

        答: 根据下图中树和数组的关系, 可以推出索引之间的转换公式.
        ```
             0          [0,
           1   2    ->   1, 2
          3 4 5 6        3, 4, 5, 6]
        ```
        父 -> 左, 右
        0  -> 1, 2
        1  -> 3, 4
        2  -> 5, 6
        ...
        n  -> 2 * n + 1, 2 * n + 2

        孩子 -> 父
        1   -> 0
        2   -> 0
        3   -> 1
        4   -> 1
        ...
        n   -> (n - 1) // 2
        """
        return index * 2 + 1

    @staticmethod
    def right_idx(index: int) -> int:
        """返回 `index` 的右孩子索引.

        公式推导参考 `left_idx`.
        """
        return index * 2 + 2

    @staticmethod
    def parent_idx(index: int) -> int:
        """返回 `index` 的父索引.

        公式推导参考 `left_idx`.
        """
        if index == 0:
            raise ValueError
        return (index - 1) // 2

    @staticmethod
    def gen_tree(iterable: Iterable) -> Optional[BTNode]:
        """由数组生成一棵树.

        注意, 由于索引是连续的, 所以数组中只能忽略最后一个叶子节点
        之后的空节点 (即图中的 6 后面的四个 None).
        ```
               1           [1,
            2    3     <-   2, 3
          4  5  N N         4, 5, None, None,
         NN N6 NN NN        None, None, None, 6]
        ```
        """
        return BTUtil._gen_tree(tuple(iterable), 0)

    @staticmethod
    def _gen_tree(array: tuple, idx: int) -> Optional[BTNode]:
        """以索引 `index` 为根生成一棵树."""
        # 空节点
        if idx > len(array) - 1 or array[idx] is None:
            return

        return BTNode(
            key=array[idx],
            val=0,
            left=BTUtil._gen_tree(array, BTUtil.left_idx(idx)),
            right=BTUtil._gen_tree(array, BTUtil.right_idx(idx))
        )


class BST:
    """二分搜索树.

    树中不允许存在重复的节点.

    可将本数据结构作为 set 使用, 在 LeetCode 804 中测试.
    可将本数据结构作为 dict 使用, 在 LeetCode 1 中测试.
    """

    def __init__(self):
        self._size: int = 0
        self._dummy_root = BTNode(None)

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: Any) -> bool:
        return self.get(key, no_value) is not no_value

    def __iter__(self) -> Iterator:
        """层序遍历."""
        return BTUtil.levelorder(self._root, filter_none=False)

    @property
    def _root(self) -> Optional[BTNode]:
        return self._dummy_root.left

    @_root.setter
    def _root(self, node: Optional[BTNode]):
        self._dummy_root.left = node

    def add(self, key: Any, value: Any = 0):
        """添加元素."""
        # 找到插入位置
        direction = 'left'
        prev = self._dummy_root
        added = getattr(prev, direction)
        while added:
            # 找到重复元素, 用新值覆盖旧值.
            if key == added.key:
                added.val = value
                return
            direction = 'left' if key < added.key else 'right'
            prev = added
            added = getattr(added, direction)

        # 条件和根为空是等价的
        setattr(prev, direction, BTNode(key, value))
        self._size += 1

    def add_with_recursion(self, key: Any, value: Any = 0):
        """添加元素."""
        self._root = self._add_with_recursion(self._root, key, value)

    def _add_with_recursion(self, root: Optional[BTNode], key: Any, value: Any) -> BTNode:
        """向以 `root` 为根的树中添加元素, 返回添加完成的树.

        怎么理解递归终止条件 ?

        答: 当 `root is None` 时, 说明找到了插入位置. 而空也是一棵树,
        向空树中插入值就等于创建一个根, 因而符合本递归函数定义.

        为什么要返回节点呢 ?

        答: 当 `root is None` 时, 说明找到了插入位置, 但连接新节点需要
        使用父节点. 如果传入父节点, 那么还需要传入插到左还是右. 而每次都返回节点,
        就可以由调用方连接节点, 被调用方就无需知道父节点了.

        与 `self.add` 之间有什么联系 ?

        答: 终止条件和 `self.add` 中 `while added` 是等价的. 而添加的节点具体接到哪里是
        由调用方决定的, 因而不需要 `self.add` 中的变量 `direction`.
        """
        # 空代表找到了插入位置
        if root is None:
            self._size += 1
            return BTNode(key, value)

        if key < root.key:
            root.left = self._add_with_recursion(root.left, key, value)
        elif key > root.key:
            root.right = self._add_with_recursion(root.right, key, value)
        # 找到重复元素, 用新值覆盖旧值.
        else:
            root.val = value
        return root

    @not_empty
    def remove(self, key: Any):
        """删除值为 `key` 的节点.

        删除情况有 3 种:

          1. 如果被删除节点是叶子节点, 父节点原本指向被删除节点的方向指向空 (根节点也可能是叶子节点, 需要特殊处理).
          2. 如果被删除节点只有右子树或只有左子树, 父节点原本指向被删除节点的方向指向右子树
             或左子树 (根节点也可能只有右子树或只有左子树, 需要特殊处理).
          3. 如果被删除节点左右子树都有, 那么找到被删除节点的右子树最小的值,
             将此值覆盖到删除节点, 然后删除这个最小节点 (由于被删除节点只是被覆盖值, 不会真正被删除, 因此不需要考虑根节点).

        1, 2 可以合并一下, 因为指向空等于指向叶子节点的右或者左.

        为什么会想到用右子树的最小值或左子树的最大值取代删除值 ?

        答: BST 在中序遍历下的结果是一个有序数组, 在有序数组中删除一个元素, 可以被理解为
           使用该元素前一个或后一个元素代替本身元素, 然后在删除前一个或后一个元素.
        """
        # 找到被删除的节点
        direction = 'left'
        prev = self._dummy_root
        delete = getattr(prev, direction)
        while delete and key != delete.key:
            direction = 'left' if key < delete.key else 'right'
            prev = delete
            delete = getattr(delete, direction)

        # `key` 不在树中
        if delete is None:
            raise ValueError

        if delete.right and delete.left:
            delete.key, delete.val, delete.left = self._pop_max_from(delete.left)
        else:
            setattr(prev, direction, delete.right or delete.left or None)
        self._size -= 1

    @not_empty
    def remove_with_recursion(self, key: Any):
        """从树中删除键为 `key` 的节点."""
        self._root = self._remove_with_recursion(self._root, key)

    def _remove_with_recursion(self, root: BTNode, key: Any) -> Optional[BTNode]:
        """从以 `root` 为根的树中删除键为 `key` 的节点, 返回删除后的树."""
        # `key` 不在树中
        if root is None:
            raise ValueError
        # 找到了删除节点
        if key == root.key:
            if root.right and root.left:
                root.key, root.val, root.left = self._pop_max_from(root.left)
                res = root
            else:
                res = root.right or root.left or None
            self._size -= 1
            return res

        if key < root.key:
            root.left = self._remove_with_recursion(root.left, key)
        else:  # key > root.key
            root.right = self._remove_with_recursion(root.right, key)
        return root

    def get(self, key: Any, default: Any = None) -> Any:
        """返回值为 `key` 的节点的值, 如果没有则返回 `default`.

        虽然看起来这个函数比较奇怪, 但当 `key` 是一个可比较对象时, 就有意义了,
        例如当 `key` 是下面用于字典的类 `Pair`.
        """
        geted = self._root
        while geted:
            if key == geted.key:
                return geted.val
            if key < geted.key:
                geted = geted.left
            else:
                geted = geted.right

        # 没找到
        return default

    @classmethod
    def from_iteralbe(cls, keys: Iterable) -> 'BST':
        tree = cls()
        for k in keys:
            tree.add(k)
        return tree

    @staticmethod
    def _pop_max_from(node: BTNode) -> Tuple[Any, Any, Optional[BTNode]]:
        """删除以 `node` 为根的树中的最大节点, 返回最大值和删除之后的树.

        最大值只可能出现于以下情况:

          1. 右叶子节点. 此时, 应将父节点的右指向空 (根节点也可以被理解为右叶子节点, 需要特殊处理).
          2. 只有左子树的节点. 此时, 应将父节点的右指向被删除节点的左子树 (根节点也可能只有左子树, 需要特殊处理).

        又因为右叶子节点的左子树必为空, 将父节点的右指向空等于指向右叶子节点的左子树,
        所以上面两条可以合并成如下情况:

          1. 找到最大节点, 将父节点的右指向该节点的左子树 (根节点也可能是最大节点, 需要特殊处理).
        """
        # 找到最大节点
        max_ = node
        prev = node
        while max_.right:
            prev = max_
            max_ = max_.right

        # `max_` 的值没有变, 证明被删除节点是根节点
        if max_.key == node.key:
            return max_.key, max_.val, max_.left
        prev.right = max_.left
        return max_.key, max_.val, node

    @staticmethod
    def _pop_max_from_with_recursion(root: BTNode) -> Tuple[Any, Any, Optional[BTNode]]:
        """删除以 `root` 为根的树中最大节点, 返回最大值和删除之后的树."""
        # 找到最大值了
        if root.right is None:
            return root.key, root.val, root.left

        k, v, n = BST._pop_max_from_with_recursion(root.right)
        root.right = n
        return k, v, n

    @staticmethod
    def is_bst(root: Optional[BTNode]) -> bool:
        """判断一棵树是否为二分搜索树.

        中序遍历是有序的就是二分搜索树.
        """
        # 空树也是合法的
        if root is None:
            return True

        vals = [n.key for n in BTUtil.inorder(root)]
        # 当只有一个元素时, 表达式等价于 all(), 而 all() is True.
        return all(vals[i] <= vals[i + 1] for i in range(0, len(vals) - 1))


class BSTDict:
    """用二分搜索树实现字典.
    本数据结构有个弊端, 由于需要底层的 `BST` 需要每个节点的值是可比较的,
    因而 `key` 必须是同一种类型, 否则将报错提示不可比较.
    """

    def __init__(self):
        self._tree = BST()

    def __repr__(self) -> str:
        return '{' + ', '.join(': '.join((repr(k), repr(v))) for k, v in self) + '}'

    def __iter__(self) -> Iterator:
        return ((node.key, node.val) for node in BTUtil.preorder(self._tree._root))

    def __len__(self) -> int:
        return len(self._tree)

    def __contains__(self, key: Any) -> bool:
        return key in self._tree

    def __setitem__(self, key: Any, value: Any):
        self._tree.add(key, value)

    def __getitem__(self, key: Any) -> Any:
        val = self._tree.get(key, no_value)
        if val is no_value:
            raise KeyError
        return val

    def __delitem__(self, key: Any):
        self._tree.remove(key)
