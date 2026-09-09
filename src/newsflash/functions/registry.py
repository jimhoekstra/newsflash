import typing
from inspect import signature
from functools import wraps

from newsflash.models import Trigger, FunctionDefinition

from .input import get_function_input_definitions


class FunctionRegistry:
    _functions: list[FunctionDefinition]

    def __init__(self) -> None:
        self._functions = []

    def _append_function(
        self, function_definition: FunctionDefinition
    ):
        self._functions.append(function_definition)

    def _set_functions(
        self, function_definitions: list[FunctionDefinition]
    ) -> None:
        self._functions = function_definitions

    def _get_functions(self) -> list[FunctionDefinition]:
        return self._functions

    def _add(
        self, on: Trigger | list[Trigger], function: typing.Callable[..., typing.Any]
    ) -> None:
        sig = signature(function)
        function_inputs = get_function_input_definitions(sig)

        if isinstance(on, list):
            triggers = on
        else:
            triggers = [on]

        function_definition = FunctionDefinition(
            func=function,
            triggers=triggers,
            inputs=function_inputs,
        )

        self._append_function(function_definition=function_definition)

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

    def combine_with(self, other: "FunctionRegistry") -> "FunctionRegistry":
        new = FunctionRegistry()
        new._set_functions(
            function_definitions=(self._get_functions() + other._get_functions()),
        )
        return new
