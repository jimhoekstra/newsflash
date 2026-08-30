import typing

from pydantic import BaseModel

from newsflash.models import Trigger

from .input import FunctionInput


class FunctionDefinition(BaseModel):
    func: typing.Callable[..., typing.Any]
    triggers: list[Trigger]
    inputs: list[FunctionInput]
