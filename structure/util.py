__all__ = (
    'check_index', 'not_empty',
)

from functools import wraps
from typing import Any, Sized


def check_index(offset: int = 0) -> callable:
    """检查索引是否在范围 [0, len + offset) 中."""
    def deco(f: callable) -> callable:
        @wraps(f)
        def wrapper(self: Sized, index: int, *args: tuple, **kwargs: dict) -> Any:
            if not (0 <= index < len(self) + offset):
                raise IndexError
            return f(self, index, *args, **kwargs)

        return wrapper

    return deco


def not_empty(f: callable) -> callable:
    """检查实例是否为空."""
    @wraps(f)
    def wrapper(self: Sized, *args: tuple, **kwargs: dict) -> Any:
        if len(self) == 0:
            raise IndexError
        return f(self, *args, **kwargs)

    return wrapper
