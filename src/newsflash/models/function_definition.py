import typing

from pydantic import BaseModel

from newsflash.models import Trigger

from .function_input_definition import FunctionInputDefinition


class FunctionDefinition(BaseModel):
    func: typing.Callable[..., typing.Any]
    triggers: list[Trigger]
    inputs: list[FunctionInputDefinition]
