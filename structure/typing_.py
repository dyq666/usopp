__all__ = (
    'Hashable',
)

from typing import Any, Protocol


class Hashable(Protocol):

    def __eq__(self, other: Any):
        ...

    def __hash__(self) -> int:
        ...
