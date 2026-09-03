import typing
from inspect import signature
from functools import wraps

from newsflash.models import Trigger, FunctionDefinition

from .input import get_function_input_definitions


class FunctionRegistry:
    _functions: list[FunctionDefinition]

    def __init__(self) -> None:
        self._functions = []

    def _add(self, on: Trigger | list[Trigger], function: typing.Callable[..., typing.Any]) -> None:
        sig = signature(function)
        function_inputs = get_function_input_definitions(sig)
    
        if isinstance(on, list):
            triggers = on
        else:
            triggers = [on]

        self._functions.append(
            FunctionDefinition(
                func=function,
                triggers=triggers,
                inputs=function_inputs,
            )
        )

    def add(self, on: Trigger | list[Trigger]):

        def decorator(function: typing.Callable[..., typing.Any]):

            self._add(
                on=on,
                function=function,
            )

            @wraps(function)
            def wrapper(*args, **kwargs):
                return function(*args, **kwargs)

            return wrapper

        return decorator
