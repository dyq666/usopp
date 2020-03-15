from typing import Any, Iterable, Optional


class ListNode:

    def __init__(self, val: Any, next_: Optional['ListNode'] = None):
        self.val = val
        self.next = next_

    def __iter__(self) -> Iterable:
        neelde = self
        while neelde is not None:
            yield neelde.val
            neelde = neelde.next

    def __len__(self) -> int:
        length = 0
        needle = self
        while needle is not None:
            length += 1
            needle = needle.next
        return length

    @classmethod
    def from_iterable(cls, values: Iterable) -> Optional['ListNode']:
        dummy = cls(None)
        needle = dummy

        for v in values:
            needle.next = cls(v)
            needle = needle.next

        return dummy.next
