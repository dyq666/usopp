from typing import Dict, Iterable, List


class Node:
    """字典树节点."""

    def __init__(self, map_: Dict[str, 'Node']):
        self.map = map_


class Trie:
    """字典树."""

    def __init__(self):
        self.root = Node({})

    def __contains__(self, item) -> bool:
        needle = self.root
        for char in item:
            if char not in needle.map:
                return False
            needle = needle.map[char]
        # 必须是叶子节点, 才算包含
        return not needle.map

    def __iter__(self) -> Iterable:
        return iter(self._words(self.root))

    def add(self, word: str):
        """添加一个单词."""
        needle = self.root
        for c in word:
            needle.map.setdefault(c, Node({}))
            needle = needle.map[c]

    @classmethod
    def from_iterable(cls, iterable: Iterable[str]) -> 'Trie':
        trie = cls()
        for word in iterable:
            trie.add(word)
        return trie

    def _words(self, root: Node) -> List[str]:
        """获得从根 `root` 到叶子的所有路径.

        和 LeetCode 257 问题类似.
        """
        if not root.map:
            return []

        words = []
        for char, child in root.map.items():
            child_words = self._words(child)
            words.extend([char + w for w in child_words] if child_words else [char])
        return words
