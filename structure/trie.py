from typing import Dict, Iterable, Iterator, List


class Node:
    """字典树节点."""

    def __init__(self, map_: Dict[str, 'Node'], is_end: bool = False):
        self.map = map_
        self.is_end = is_end


class Trie:
    """字典树."""

    def __init__(self):
        self.root = Node({})

    def __contains__(self, item: str) -> bool:
        needle = self.root
        for char in item:
            if char not in needle.map:
                return False
            needle = needle.map[char]
        # 必须是叶子节点, 才算包含
        return needle.is_end

    def __iter__(self) -> Iterator:
        return iter(self._words(self.root))

    def add(self, word: str):
        """添加一个单词."""
        needle = self.root
        for c in word:
            needle.map.setdefault(c, Node({}))
            needle = needle.map[c]
        needle.is_end = True

    @classmethod
    def from_iterable(cls, iterable: Iterable[str]) -> 'Trie':
        trie = cls()
        for word in iterable:
            trie.add(word)
        return trie

    def _words(self, root: Node) -> List[str]:
        """返回从根 `root` 到标记了 `is_end` 节点的所有路径.

        递归终止条件是隐式的, 当 `root.map` 为空字典时, 不会递归调用.

        和 LeetCode 257 问题类似.
        """
        words = []
        for char, child in root.map.items():
            child_words = self._words(child)
            if child:
                words.extend([char + w for w in child_words])
            if child.is_end:
                words.append(char)
        return words
