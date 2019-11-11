"""
AUTHOR: dyq666
DATE: 2018.7.24
提供一些创建数据结构时需要使用的装饰器
1. 在函数前, 检验索引是否合法
2. 在函数后, 更改数据结构中元素的个数
3. 在函数前, 检验数据结构是否为空
"""

from inspect import signature
from functools import wraps


def index_valid(left, right):
    """
    功能：传入字符串left, right, 判断方法中的index参数是否在[left, right]之间
    1. 得到原函数的定义时的参数名
    2. 获取参数self, index(如果函数中没有该)的位置, 然后从args中获取值, 如果没有就报ValueError
    3. 传入的参数为字符串, 使用eval执行字符串得到值(原因是需要使用self, 但是实例方法绑定装饰器时不能获取到self)
    4. 判断index是否在[left, right]之间
    """
    def decorate(func):
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 1. 得到原函数的定义时的参数名
            params = list(signature(func).parameters.keys())
            try:
                # 2. 得到类实例和得到索引值
                self, index = args[params.index('self')], args[params.index('index')]
            except ValueError as e:
                raise e
            else:
                # 3. 执行字符串得到边界
                inner_left = eval(left)
                inner_right = eval(right)

                # 4. 判断边界是否符合
                if not inner_left <= index <= inner_right:
                    raise ValueError(f"Index must in [{inner_left}...{inner_right}]")

            return func(*args, **kwargs)
        return wrapper

    return decorate


def size_change(move_num):
    """
    功能：在最后对数据结构中的大小进行改变, 必须保证数据结构中的size名为__size
    1. 获取参数self
    2. 改变size的大小
    """
    def decorator(func):
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)

            self = args[0]
            self._size += move_num

            return res
        return wrapper

    return decorator


def non_empty(func):
    """
    功能: 判断类实例是否为空
    限制: 实例必须支持bool或len
    """
    @wraps(func)
    def wrapper(*args, **kwargs):

        self = args[0]
        if not self:
            raise ValueError('Cannot get a value from a empty datas')
            
        return func(*args, **kwargs)
    return wrapper
    