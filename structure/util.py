__all__ = (
    'check_index', 'no_value', 'not_empty', 'size_change',
)

from functools import wraps
from typing import Any, Sized

no_value = object()


def check_index(offset: int = 0) -> callable:
    """在运行函数前, 检查索引是否在范围 [0, len + offset) 中."""
    def deco(f: callable) -> callable:
        @wraps(f)
        def wrapper(self: Sized, index: int, *args: tuple, **kwargs: dict) -> Any:
            if not (0 <= index < len(self) + offset):
                raise IndexError
            return f(self, index, *args, **kwargs)

        return wrapper

    return deco


def not_empty(f: callable) -> callable:
    """在运行函数前, 检查实例是否为空."""
    @wraps(f)
    def wrapper(self: Sized, *args: tuple, **kwargs: dict) -> Any:
        if len(self) == 0:
            raise IndexError('pop from empty structure')
        return f(self, *args, **kwargs)

    return wrapper


def size_change(delta: int) -> callable:
    """在运行函数后, 修改 `self._size`."""
    def deco(f: callable) -> callable:
        @wraps(f)
        def wrapper(self, *args: tuple, **kwargs: dict) -> Any:
            res = f(self, *args, **kwargs)
            self._size += delta
            return res

        return wrapper

    return deco
