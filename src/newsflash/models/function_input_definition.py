import typing

from pydantic import BaseModel

from .element import Element


class FunctionInputDefinition(BaseModel):
    arg_name: str
    element_type: typing.Type[Element]
    element_id: str
