class ListNode:

    def __init__(self, val):
        self.val = val
        self.next = None

    def __iter__(self):
        needle = self
        while needle:
            yield needle
            needle = needle.next

    def __repr__(self):
        return f'<{self.__class__.__name__} val={self.val}>'

    @classmethod
    def from_list(cls, values: list):
        dummy_head = cls(None)

        needle = dummy_head
        for v in values:
            needle.next = cls(v)
            needle = needle.next
        return dummy_head.next
