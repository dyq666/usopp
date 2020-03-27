from typing import Dict, Iterable, Iterator, List


class Node:
    """字典树节点."""

    def __init__(self, children: Dict[str, 'Node'], is_end: bool = False):
        self.children = children
        self.is_end = is_end


class Trie:
    """字典树.

    字典树中的节点不存储值, 值都存在父节点的字典中.
    """

    def __init__(self):
        self.root = Node({})
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def __contains__(self, word: str) -> bool:
        needle = self.root
        for char in word:
            if char not in needle.children:
                return False
            needle = needle.children[char]
        return needle.is_end

    def __iter__(self) -> Iterator:
        return iter(self._words(self.root))

    def add(self, word: str):
        needle = self.root
        for char in word:
            needle.children.setdefault(char, Node({}))
            needle = needle.children[char]
        if not needle.is_end:
            needle.is_end = True
            self.size += 1

    @classmethod
    def from_iterable(cls, iterable: Iterable[str]) -> 'Trie':
        trie = cls()
        for word in iterable:
            trie.add(word)
        return trie

    def _words(self, root: Node) -> List[str]:
        """返回从根 `root` 到标记了 `is_end` 节点的所有路径.

        递归终止条件是隐式的, 当 `root.children` 为空字典时, 不会递归调用.

        和 LeetCode 257 问题类似.
        """
        words = []
        for char, child in root.children.items():
            if child.is_end:
                words.append(char)
            words.extend([char + w for w in self._words(child)])
        return words
