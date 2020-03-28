__all__ = (
    'UnionFind',
)


class UnionFind:
    """并查集"""

    def __init__(self):
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def is_connected(self, p: int, q: int) -> bool:
        pass

    def union(self, p: int, q: int):
        pass
