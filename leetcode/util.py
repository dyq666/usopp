from typing import Any, Iterable, Optional


class ListNode:

    def __init__(self, x: Any, next_: Optional['ListNode'] = None):
        self.val = x
        self.next = next_

    def __iter__(self):
        neelde = self
        while neelde is not None:
            yield neelde.val
            neelde = neelde.next

    @classmethod
    def from_iterable(cls, values: Iterable) -> 'ListNode':
        dummy = cls(None)
        needle = dummy

        for v in values:
            needle.next = cls(v)
            needle = needle.next

        return dummy.next
