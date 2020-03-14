__all__ = (
    'check_index', 'not_empty',
)

from functools import wraps
from typing import Any, Callable, Sized


def check_index(offset: int = 0) -> Callable:
    """在执行数据结构某个方法前检查索引是否有效.

    方法必须满足第一个参数是 `self`, 第二是索引, 同时类必须实现 `__len__`.

    索引的检查范围是 [0, len + offset).
    """
    def deco(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(self: Any, index: int, *args, **kwargs):
            if not (0 <= index < len(self) + offset):
                raise IndexError
            return f(self, index, *args, **kwargs)

        return wrapper

    return deco


def not_empty(f: Callable) -> Callable:
    """在执行数据结构某个方法前检查数据结构是否为空."""
    @wraps(f)
    def wrapper(self: Sized, *args, **kwargs):
        if len(self) == 0:
            raise IndexError
        return f(self, *args, **kwargs)

    return wrapper
