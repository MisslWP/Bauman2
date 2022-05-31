from typing import Union, TypeVar, Callable, Generic

T = TypeVar('T')


class Property(Generic[T]):

    def __init__(self, val: Union[Callable[..., T], T], const: bool = True) -> None:
        self.const: bool = const
        self.__val: Union[T, Callable[..., T]] = val

    @staticmethod
    def func(f: Callable[..., T]):
        return Property(f, False)

    def value(self, *args, **kwargs) -> T:
        if self.const:
            return self.__val
        else:
            return self.__val(*args, **kwargs)
