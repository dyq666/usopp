__all__ = (
    'Trie',
)

from typing import Dict, Iterable, Iterator, List, Optional


class Node:
    """字典树节点.

    `is_end`: 代表此节点是一个单词的末尾.
    """

    def __init__(self, children: Optional[Dict[str, 'Node']] = None,
                 is_end: bool = False):
        self.children = {} if children is None else children
        self.is_end = is_end


class Trie:
    """字典树.

    字典树中的节点本身不存储值, 它的值存储在父节点的字典中, 因此部分逻辑和
    一般的树结构有些区别.

    可用 LeetCode 208 测试.
    """

    def __init__(self):
        self.root: Node = Node()
        self.size: int = 0

    def __len__(self) -> int:
        return self.size

    def __contains__(self, word: str) -> bool:
        cur = self.root
        for char in word:
            if char not in cur.children:
                return False
            cur = cur.children[char]
        return cur.is_end

    def __iter__(self) -> Iterator:
        return iter(self._words(self.root))

    def add(self, word: str):
        cur = self.root
        for char in word:
            cur.children.setdefault(char, Node())
            cur = cur.children[char]
        if not cur.is_end:
            cur.is_end = True
            self.size += 1

    def startswith(self, prefix: str) -> bool:
        """是否有 `prefix` 前缀.

        和 `__contains__` 逻辑基本一致, 除了最后不需要判断节点是否终止.
        """
        cur = self.root
        for char in prefix:
            if char not in cur.children:
                return False
            cur = cur.children[char]
        return True

    @classmethod
    def from_iterable(cls, iterable: Iterable[str]) -> 'Trie':
        trie = cls()
        for word in iterable:
            trie.add(word)
        return trie

    def _words(self, root: Node) -> List[str]:
        """返回从根 `root` 到所有终止节点的所有路径.

        和 LeetCode 257 问题类似.
        """
        # 实际上这里的递归终止条件是可以省略的, 下面的遍历隐含
        # 终止条件: 当 `root.children` 为空时, 递归终止.
        if not root.children:
            return []

        words = []
        for char, child in root.children.items():
            if child.is_end:
                words.append(char)
            words.extend([char + w for w in self._words(child)])
        return words
