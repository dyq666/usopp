__all__ = ()

from typing import Any


class StudentV1:

    def __init__(self, grade: int, class_: int, name: str):
        self.grade = grade
        self.class_ = class_
        self.name = name


class StudentV2:

    def __init__(self, grade: int, class_: int, name: str):
        self.grade = grade
        self.class_ = class_
        self.name = name

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.grade == other.grade
            and self.class_ == other.class_
            and self.name == other.name
        )

    def __hash__(self) -> int:
        # hash = self.grade * B^2 + self.class_ * B^1 + hash(self.name) * B^0
        # hash = (self.grade * B + self.class_) * B + hash(self.name)
        val = 0
        for attr in (self.grade, self.class_, hash(self.name)):
            # B 实际上可以是任意值, 这里选用 B = 26.
            val = val * 26 + attr
        return val


def test_student():
    studentv1_a1 = StudentV1(1, 2, 'aaa')
    studentv1_a2 = StudentV1(1, 2, 'aaa')
    assert studentv1_a1 != studentv1_a2
    assert studentv1_a1 is not studentv1_a2
    assert len({studentv1_a1, studentv1_a2}) == 2

    studentv2_a1 = StudentV2(1, 2, 'aaa')
    studentv2_a2 = StudentV2(1, 2, 'aaa')
    assert studentv2_a1 == studentv2_a2
    assert studentv2_a1 is not studentv2_a2
    assert len({studentv2_a1, studentv2_a2}) == 1
