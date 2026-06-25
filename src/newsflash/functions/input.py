import typing
from inspect import Signature

from pydantic import BaseModel

from newsflash.elements.base import Element


class FunctionInput(BaseModel):
    arg_name: str
    element_type: typing.Type[Element]
    element_query: str


def build_function_input(arg_name: str, annotation: typing.Any) -> FunctionInput:
    origin = typing.get_origin(annotation)
    if origin != typing.Annotated:
        raise ValueError("type is not annotated")

    args = typing.get_args(annotation)
    id_arg = args[1]

    return FunctionInput(
        arg_name=arg_name,
        element_type=args[0],
        element_query=id_arg,
    )


def get_function_inputs(func_signature: Signature) -> list[FunctionInput]:
    function_inputs: list[FunctionInput] = []
    for arg_name, arg in func_signature.parameters.items():
        function_inputs.append(
            build_function_input(arg_name=arg_name, annotation=arg.annotation)
        )

    return function_inputs
