import typing
from inspect import signature
from functools import wraps

from newsflash.elements.base import Trigger

from .function_definition import FunctionDefinition
from .input import get_function_inputs


class FunctionRegistry:
    functions: list[FunctionDefinition]

    def __init__(self) -> None:
        self.functions = []

    def add(self, on: Trigger | list[Trigger]):

        def decorator(func: typing.Callable[..., typing.Any]):

            sig = signature(func)
            function_inputs = get_function_inputs(sig)
            if isinstance(on, list):
                triggers = on
            else:
                triggers = [on]

            self.functions.append(
                FunctionDefinition(
                    func=func,
                    triggers=triggers,
                    inputs=function_inputs,
                )
            )

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator
