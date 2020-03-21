__all__ = (
    'BST', 'BTNode', 'BTUtil'
)

from itertools import chain, zip_longest
from typing import Any, Generator, List, Iterable, Optional

from util import not_empty


class BTNode:
    """二叉树节点. (BT -> BinaryTree)"""

    def __init__(self, val: Any,
                 left: Optional['BTNode'] = None,
                 right: Optional['BTNode'] = None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__}'
            f' val={self.val!r}'
            f'>'
        )

    @classmethod
    def from_iterable(cls, data: Iterable) -> Optional['BTNode']:
        """根据数组生成一棵树.

        如下图所示, 层序遍历树生成数组.
        ```
            1          [1,
          2   3    ->   2, 3,
         4 5 空 6       4, 5, None, 40]
        ```

        数组依照索引生成树, 由上图可知父索引和子索引关系:
          - 0: 1, 2
          - 1: 3, 4
          - 2: 5, 6
            ...
          - n: (n + 1) * 2 - 1, (n + 1) * 2

        由于索引是连续的, 所以数组中只有最后一层的空节点可以省略.
        ```
              1           [1,
            2   3     ->   2, 3
          4  5             4, 5, None, None,
        空空 空6            None, None, 6]
        ```
        """
        return cls._gen_tree(tuple(data), 0)

    @classmethod
    def _gen_tree(cls, data: tuple, index: int) -> Optional['BTNode']:
        """以 `index` 索引作为根节点生成一棵树 (`cls.from_list` 的递归函数)."""
        if index >= len(data) or data[index] is None:
            return

        node = cls(data[index])
        node.left = cls._gen_tree(data, (index + 1) * 2 - 1)
        node.right = cls._gen_tree(data, (index + 1) * 2)
        return node


class BTUtil:
    """二叉树常用操作. (BT -> BinaryTree)"""

    @classmethod
    def preorder(cls, root: Optional[BTNode], skip_none: bool = True
                 ) -> Generator[Optional[BTNode], None, None]:
        """前序遍历.

        `skip_none`: 非叶子节点的空子节点是否返回.

        为什么前序遍历会想到用栈而不是队列呢 ?

        答: 因为栈可以插队, 而队列不行. 当遍历到某个节点时, 需要存储节点的左右节点,
        如果使用队列, 下两次出队肯定是这两个节点, 而前序遍历需要先遍历左子树再遍历右子树.
        使用栈时, 可以右节点先入栈, 左节点再入栈, 取出左节点, 将左节点的子节点入栈,
        这时左子节点就插到了右节点的前面.

        如何看待迭代实现和递归实现二者的异同 ?

        答: 实际上二者逻辑类似. 假设函数的每条语句存储到栈中执行, 那么最后一条语句
        一定在栈底. `preorder_with_mocked_stack` 中模拟系统栈实现了前序遍历,
        栈中的顺序和 `preorder_with_recursion` 的语句是对应的, 1 代表 `yield xx`
        0 代表 `yield from cls.preorder_with_recursion_and_none`.
        而 `node and node.right` 实际上就是递归中的终止条件 `if not root: return`.

        `preorder` 和 `preorder_with_mocked_stack` 的区别 ?

        答: `preorder_with_mocked_stack` 更容易理解, 更容易转换成中序和后序遍历.
        而 `preorder` 只针对前序遍历的优化实现, 减少了入栈出栈的次数, 因而不能扩展到中序和后序,
        当然, 中序和后序都有自己的优化实现.
        """
        if not root:
            return

        nodes = [root]
        while nodes:
            node = nodes.pop()
            yield node
            if skip_none:
                nodes.extend(n for n in (node.right, node.left) if n)
            else:
                if node and not cls.isleaf(node):
                    nodes.extend(n for n in (node.right, node.left))

    @classmethod
    def inorder(cls, root: Optional[BTNode]) -> Generator[BTNode, None, None]:
        """中序遍历.

        中序遍历的验证可使用 LeetCode 538.

        TODO 研究为什么要这么做, 怎么从递归转换来的.
        """

        def _left_side(n: BTNode) -> Iterable:
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
    def postorder(cls, root: Optional[BTNode]) -> Generator[BTNode, None, None]:
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
    def levelorder(cls, root: Optional[BTNode], skip_none: bool = True
                   ) -> Generator[List[Optional[BTNode]], None, None]:
        """层序遍历 (每次都返回一层的节点).

        `skip_none`: 非叶子节点的空子节点是否返回.

        层序遍历通常使用队列, 为什么这里用的是 list, list 应该只能用做栈 ?

        答: 虽然这里用的是 list, 但实际上还是先进先出, 只不过这里先进先出的特性是由
        遍历完成的 (先放进 list 的先被访问).
        """
        if not root:
            return

        nodes = [root]
        while nodes:
            yield nodes
            if skip_none:
                nodes = [child
                         for n in nodes
                         for child in (n.left, n.right) if child]
            else:
                nodes = (n for n in nodes if n and not cls.isleaf(n))
                nodes = list(chain.from_iterable((n.left, n.right)
                                                 for n in nodes
                                                 if n and not cls.isleaf(n)))

    @classmethod
    def is_equal(cls, one: Optional[BTNode],
                 other: Optional[BTNode]) -> bool:
        """判断两棵树是否相同.

        这里可用任意遍历方式, 但无论哪种都必须返回非叶子节点的空子节点 (实际上返回包括
        叶子节点的空子节点也是可以的, 只不过如果一棵树所有叶子节点相同, 那么这些叶子节
        点的子节点也肯定是相同的).

        此外, 可以用 LeetCode 100 测试.
        """
        for n1, n2 in zip_longest(cls.preorder(one, skip_none=False),
                                  cls.preorder(other, skip_none=False)):
            v1 = n1 and n1.val
            v2 = n2 and n2.val
            if v1 != v2:
                return False
        return True

    @classmethod
    def isleaf(cls, node: Optional[BTNode]) -> bool:
        """是否为叶子节点."""
        return bool(node and node.left is None and node.right is None)

    @classmethod
    def preorder_with_mocked_stack(cls, root: Optional[BTNode]
                                   ) -> Generator[BTNode, None, None]:
        """模拟系统栈实现前序遍历.

        `nodes` 中存储的结构为 (操作码, 节点), 操作码有 0, 1 两种, 其中 0 代表遍历, 1 代表返回.

        另外, 只要改变入栈顺序就可以换成中序和后序.
        """
        if not root:
            return

        nodes = [(0, root)]
        while nodes:
            operator, node = nodes.pop()
            if operator == 0:
                # 这里可以改为 nodes.extend((o, n) for o, n in ((0, node.right), (0, node.left), (1, node)) if n)
                # 不过为了和 `preorder_with_mocked_stack_and_none` 对比, 选择了分别 append 的方式.
                operators = []
                # 这个方法中 `node` 只会是 `BTNode`, 因此可以不检查空.
                if node.right:
                    operators.append((0, node.right))
                if node.left:
                    operators.append((0, node.left))
                operators.append((1, node))
                nodes.extend(operators)
            else:
                yield node

    @classmethod
    def preorder_with_mocked_stack_and_none(cls, root: Optional[BTNode]
                                            ) -> Generator[Optional[BTNode], None, None]:
        """模拟系统栈实现前序遍历 (返回非叶子节点的空节点)."""
        if not root:
            return

        nodes = [(0, root)]
        while nodes:
            operator, node = nodes.pop()
            if operator == 0:
                operators = []
                if node and (node.right or not cls.isleaf(node)):
                    operators.append((0, node.right))
                if node and (node.left or not cls.isleaf(node)):
                    operators.append((0, node.left))
                operators.append((1, node))
                nodes.extend(operators)
            else:
                yield node

    @classmethod
    def preorder_with_recursion(cls, root: Optional[BTNode]
                                ) -> Generator[BTNode, None, None]:
        """递归实现前序遍历.

        另外, 只要改变语句顺序就可以换成中序和后序.
        """
        if not root:
            return

        yield root
        yield from cls.preorder_with_recursion(root.left)
        yield from cls.preorder_with_recursion(root.right)

    @classmethod
    def preorder_with_recursion_and_none(cls, root: Optional[BTNode],
                                         father_is_leaf: bool = True
                                         ) -> Generator[Optional[BTNode], None, None]:
        """递归实现前序遍历, 同时返回非叶子节点的空节点.

        `father_is_leaf`: 实际上这个函数拆成两个函数, 一个面向使用者, 一个用于递归. 因为 `father_is_leaf`
                          并不需要提供给使用者. 默认值为 `True` 是因为当根节点为 None 时, 希望返回一个空
                          的迭代器.
        """
        if not root:
            if not father_is_leaf:
                yield root
            return

        yield root
        yield from cls.preorder_with_recursion_and_none(root.left, cls.isleaf(root))
        yield from cls.preorder_with_recursion_and_none(root.right, cls.isleaf(root))


class BST:
    """二分搜索树. (BST -> BinarySearchTree)

    树中不存在重复元素.
    """

    def __init__(self):
        self._size: int = 0
        self.root: Optional[BTNode] = None

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterable:
        return BTUtil.preorder(self.root, skip_none=False)

    def add(self, value: Any):
        """添加元素."""
        if self.root is None:
            self.root = BTNode(value)
            self._size += 1
            return

        needle = self.root
        while True:
            if value < needle.val:
                if needle.left is None:
                    needle.left = BTNode(value)
                    self._size += 1
                    break
                needle = needle.left
            elif value > needle.val:
                if needle.right is None:
                    needle.right = BTNode(value)
                    self._size += 1
                    break
                needle = needle.right
            else:  # value == needle.val
                break

    def add_with_recursion(self, value: Any):
        """递归添加元素."""
        self.root = self._add_with_recursion(self.root, value)

    def _add_with_recursion(self, node: Optional[BTNode], value: Any) -> BTNode:
        """向以 `node` 为根的树中插入 `value`, 返回插入后的根.
        (`add_with_recursion` 的递归函数)

        怎么理解递归终止条件 ?

        答: 当 `node is None` 时, 说明找到了插入位置. 而空也是一棵树,
        向空树中插入值就等于创建一个新节点, 因而符合本递归函数定义.

        为什么要返回节点呢 ?

        答: 当 `node is None` 时, 说明找到了插入位置, 但连接新节点需要
        使用父节点. 如果传入父节点, 那么还需要传入插到左还是右. 而每次都返回节点,
        就可以由调用方连接节点, 被调用方就无需知道父节点了. 另外, 还有一种方法是
        使递归终止于被插入值的父节点, 但这种办法需要频繁的检查空. `add_with_recursion2`
        实现了这种方法.
        """
        if node is None:
            self._size += 1
            return BTNode(value)

        if value < node.val:
            node.left = self._add_with_recursion(node.left, value)
        elif value > node.val:
            node.right = self._add_with_recursion(node.right, value)
        return node

    def add_with_recursion2(self, value: Any):
        if self.root is None:
            self.root = BTNode(value)
            self._size += 1
            return
        self._add_with_recursion2(self.root, value)

    def _add_with_recursion2(self, node: BTNode, value: Any):
        """向以 `node` 为根的树中插入 `value`, 树不能为空."""
        if value < node.val and node.left is None:
            node.left = BTNode(value)
            self._size += 1
            return
        if value > node.val and node.right is None:
            node.right = BTNode(value)
            self._size += 1
            return
        if value == node.val:
            return

        if value < node.val:
            self._add_with_recursion2(node.left, value)
        elif value > node.val:
            self._add_with_recursion2(node.right, value)

    @not_empty
    def pop_max(self) -> Any:
        """删除最大值.

        实际上会遇到四种情况:

          1. 被删除节点是根节点, 且树中只有一个节点, 因而也是叶子节点. 应将根节点指向空.
          2. 被删除节点不是根节点是叶子节点. 应将父节点的右指向空 (因为最大值永远在右边, 所以被删除节点只可能是右叶子节点).
          3. 被删除节点是根节点, 根节点有左子树. 应将根节点指向左子树 (因为最大值永远在右边, 所以当删除根节点时, 根节点有且仅有左子树).
          4. 被删除节点不是根节点不是叶子节点. 应将父节点的右指向删除节点的左节点 (因为最大值永远在右边, 被删除节点有且仅有左子树).

        其中 1, 3 可以合并, 因为叶子的节点的左节点是空, 所以 *应将根节点指向空* 等价于 *应将根节点指向根节点的左节点*.
        同理 2, 4 也可以合并.

        :) 如果树能像链表一样使用 dummy_root, 这四种情况就可以合成一种了.
        """
        # 找到最右边的节点
        prev = self.root
        delete = self.root
        while delete.right:
            prev = delete
            delete = prev.right

        if self.is_root(delete):
            self.root = delete.left
        else:
            prev.right = delete.left
        self._size -= 1
        return delete.val

    @not_empty
    def pop_max_with_recursion(self) -> Any:
        """递归的删除最大值.

        递归函数的思路和 `_add_with_recursion` 类似.

        此外, 由于递归需要拼接节点, 所以不容易返回被删除节点的值, 因而这里会
        先去找到最大值.
        """
        needle = self.root
        while needle.right:
            needle = needle.right

        self.root = self._pop_max_with_recursion(self.root)
        return needle.val

    def _pop_max_with_recursion(self, node: BTNode) -> Optional[BTNode]:
        if node.right is None:
            self._size -= 1
            return node.left

        node.right = self._pop_max_with_recursion(node.right)
        return node

    @not_empty
    def pop_min(self) -> Any:
        """删除最小值.

        基本原理和 `pop_max` 相同.
        """
        prev = self.root
        delete = self.root
        while delete.left:
            prev = delete
            delete = prev.left

        if self.is_root(delete):
            self.root = delete.right
        else:
            prev.left = delete.right
        self._size -= 1
        return delete.val

    @not_empty
    def pop_min_with_recursion(self) -> Any:
        """递归的删除最小值, 和 `pop_max_with_recursion` 类似."""
        needle = self.root
        while needle.left:
            needle = needle.left

        self.root = self._pop_min_with_recursion(self.root)
        return needle.val

    def _pop_min_with_recursion(self, node: BTNode) -> Optional[BTNode]:
        if node.left is None:
            self._size -= 1
            return node.right

        node.left = self._pop_min_with_recursion(node.left)
        return node

    def is_root(self, node: Optional[BTNode]) -> bool:
        """判断节点是否为根节点."""
        return bool(node and self.root and node.val == self.root.val)
