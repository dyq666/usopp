__all__ = (
    'Comparable', 'Equable', 'Hashable',
)

from typing import Any, Protocol


class Comparable(Protocol):

    def __eq__(self, other: Any):
        ...

    def __gt__(self, other: Any):
        ...


class Equable(Protocol):

    def __eq__(self, other: Any):
        ...


class Hashable(Protocol):

    def __eq__(self, other: Any):
        ...

    def __hash__(self) -> int:
        ...
