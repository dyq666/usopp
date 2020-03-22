__all__ = (
    'BST', 'BTNode', 'BTUtil'
)

from functools import total_ordering
from itertools import chain, zip_longest
from typing import Any, Generator, List, Iterable, Optional, Tuple

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

    树中不允许存在重复元素.

    可将本数据结构当做 set, 用 LeetCode 804 测试.
    """

    def __init__(self):
        self._size: int = 0
        self.root: Optional[BTNode] = None

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterable:
        return BTUtil.inorder(self.root)

    def add(self, value: Any):
        """添加元素.

        :) 如果能用 dummy_root 就能简化一些代码了 !
        """
        # 找到插入位置
        prev = self.root
        added = self.root
        direction = None
        while added:
            # 重复元素时, 用新值覆盖旧值, 具体原因是为字典服务.
            # 当 `value` 是一个类实例, 相等不代表他们真的都一样, 例如类 `Pair`.
            if value == added.val:
                added.val = value
                return

            prev = added
            if value < added.val:
                added = added.left
                direction = 'left'
            else:
                added = added.right
                direction = 'right'

        # 代表根节点为空
        if direction is None:
            self.root = BTNode(value)
        else:
            setattr(prev, direction, BTNode(value))
        self._size += 1

    def add_with_recursion(self, value: Any):
        """`add` 方法的递归实现."""
        self.root = self._add_with_recursion(self.root, value)

    def _add_with_recursion(self, node: Optional[BTNode], value: Any) -> BTNode:
        """向以 `node` 为根的树中添加 `value`, 返回添加完成的树.

        怎么理解递归终止条件 ?

        答: 当 `node is None` 时, 说明找到了插入位置. 而空也是一棵树,
        向空树中插入值就等于创建一个新节点, 因而符合本递归函数定义.

        为什么要返回节点呢 ?

        答: 当 `node is None` 时, 说明找到了插入位置, 但连接新节点需要
        使用父节点. 如果传入父节点, 那么还需要传入插到左还是右. 而每次都返回节点,
        就可以由调用方连接节点, 被调用方就无需知道父节点了.

        与 `self.add` 之间有什么联系 ?

        答: 终止条件和 `self.add` 中 `while added` 是等价的. 而添加的节点具体接到哪里是
        由调用方决定的, 因而不需要 `self.add` 中的变量 `direction`.
        """
        # 空代表找到了插入位置
        if node is None:
            self._size += 1
            return BTNode(value)

        if value < node.val:
            node.left = self._add_with_recursion(node.left, value)
        elif value > node.val:
            node.right = self._add_with_recursion(node.right, value)
        else:  # value == node.val
            node.val = value
        return node

    @not_empty
    def remove(self, value: Any):
        """删除值为 `value` 的节点.

        删除情况有四种:

          1. 如果被删除节点是叶子节点, 父节点原本指向被删除节点的方向指向空 (根节点也是叶子节点, 需要特殊处理).
          2. 如果被删除节点只有右子树, 父节点原本指向被删除节点的方向指向右子树 (根节点也可能只有右子树, 需要特殊处理).
          3. 如果被删除节点只有左子树, 父节点原本指向被删除节点的方向指向左子树 (根节点也可能只有左子树, 需要特殊处理).
          4. 如果被删除节点左右子树都有, 那么找到被删除节点的右子树最小的值,
             将此值覆盖到删除节点, 然后删除这个最小节点 (由于被删除节点只是被覆盖值, 不会真正被删除, 因此不需要考虑根节点).

        2, 3, 4 还能整合一下. 4 实际上有两种办法删除节点, 找右子树的最小值或找左子树的最大值.
        而 2 可以转换为找右子树的最小值, 3 可以转换为找左子树的最大值. 因此将规则合并为:

          1. 如果被删除节点是叶子节点, 父节点原本指向被删除节点的方向指向空 (根节点也是叶子节点, 需要特殊处理).
          2. 如果被删除节点有右子树, 删除右子树中的最小值, 将最小值赋给被删除节点.
          3. 如果被删除节点有左子树, 删除左子树中的最大值, 将最大值赋给被删除节点.

        实际上, 合并之后的规则虽然清晰了, 但耗时增加了. 因为之前只有右子树或只有左子树的情况, 删除是 O(1) 的,
        而找最小值或最大值是 O(logN). 所以理论上不应该合并规则的, 但这里牺牲了时间复杂度, 提高了可读性.

        为什么可以用右子树的最小值或左子树的最大值取代删除值 ?

        答: BST 在中序遍历下的结果是一个有序数组, 在有序数组中删除一个元素, 可以被理解为
        使用该元素前一个或后一个元素代替本身元素, 然后在删除前一个或后一个元素.
        """
        # 找到被删除的节点
        prev = self.root
        delete = self.root
        direction = None
        while delete and value != delete.val:
            if value < delete.val:
                direction = 'left'
                prev = delete
                delete = prev.left
            else:
                direction = 'right'
                prev = delete
                delete = prev.right

        # `value` 不在树中
        if delete is None:
            raise ValueError

        if BTUtil.isleaf(delete):
            if direction is None:
                self.root = None
            else:
                setattr(prev, direction, None)
        elif delete.right:
            delete.val, delete.right = self._pop_min_from(delete.right)
        else:  # elif delete.left
            delete.val, delete.left = self._pop_max_from(delete.left)
        self._size -= 1

    @not_empty
    def remove_with_recursion(self, value: Any):
        """`remove` 方法的递归实现."""
        self.root = self._remove_with_recursion(self.root, value)

    def _remove_with_recursion(self, node: BTNode, value: Any) -> Optional[BTNode]:
        """从 `node` 中删除值为 `value` 的节点, 返回删除完成的树."""
        # 树中没有 `value`
        if node is None:
            raise ValueError
        # 找到了删除节点
        if value == node.val:
            if BTUtil.isleaf(node):
                self._size -= 1
                return
            if node.right:
                node.val, node.right = self._pop_min_from(node.right)
            else:  # elif node.left
                node.val, node.left = self._pop_max_from(node.left)
            self._size -= 1
            return node

        if value < node.val:
            node.left = self._remove_with_recursion(node.left, value)
        else:  # val > node.val
            node.right = self._remove_with_recursion(node.right, value)
        return node

    @classmethod
    def from_iteralbe(cls, values: Iterable) -> 'BST':
        tree = cls()
        for v in values:
            tree.add(v)
        return tree

    @staticmethod
    def _pop_max_from(node: BTNode) -> Tuple[Any, Optional[BTNode]]:
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
        if max_.val == node.val:
            return max_.val, max_.left
        prev.right = max_.left
        return max_.val, node

    @staticmethod
    def _pop_max_from_with_recursion(node: BTNode) -> Tuple[Any, Optional[BTNode]]:
        """删除以 `node` 为根的树中的最大节点, 返回最大值和删除之后的树.

        `_pop_max_from` 的递归实现.

        `_pop_max_from_with_recursion`, `_pop_max_from` 之间的联系和
        `add_with_recursion`, `add` 之间的联系类似.
        """
        # 找到最大值了
        if node.right is None:
            return node.val, node.left

        v, n = BST._pop_max_from_with_recursion(node.right)
        node.right = n
        return v, n

    @staticmethod
    def _pop_min_from(node: BTNode) -> Tuple[Any, Optional[BTNode]]:
        """删除以 `node` 为根的树中的最小节点, 返回最小值和删除之后的树.

        基本原理和 `_pop_max_from` 相同.
        """
        # 找到最小节点
        min_ = node
        prev = node
        while min_.left:
            prev = min_
            min_ = min_.left

        # `min_` 的值没有变, 证明被删除节点是根节点
        if min_.val == node.val:
            return min_.val, node.right
        prev.left = min_.right
        return min_.val, node


@total_ordering
class Pair:
    """二分搜索树从集合转为字典的辅助类.

    由于 `BST` 中只能存放一个值, 不能直接用于字典. 一种方式是让 `BTNode`
    存放 key, value, 然后重写 `BST`, 但这种方式代价比较高. 另一种方式是
    `BST` 中存放一个可比较的类实例, 将 key, value 存放到这个类实例中即可.
    """

    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}'
            f' key={self.key!r}'
            f' value={self.value!r}'
            f'>'
        )

    def __eq__(self, other: 'Pair') -> bool:
        return self.key == other.key

    def __gt__(self, other: 'Pair') -> bool:
        return self.key > other.key


class BSTDict:
    """用二分搜索树实现字典."""

    def __init__(self):
        self.tree = BST()

    def __iter__(self) -> Iterable:
        return ((node.val.key, node.val.value) for node in self.tree)

    def add(self, key: Any, value: Any):
        self.tree.add(Pair(key, value))

    def remove(self, key: Any):
        self.tree.remove(Pair(key, None))
