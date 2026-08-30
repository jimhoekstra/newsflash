import typing
from inspect import Signature

from pydantic import BaseModel, ValidationError

from newsflash.models import Element, ID


class FunctionInput(BaseModel):
    arg_name: str
    element_type: typing.Type[Element]
    element_id: str


def build_function_input(arg_name: str, annotation: typing.Any) -> FunctionInput:
    origin = typing.get_origin(annotation)

    if origin == typing.Annotated:
        args = typing.get_args(annotation)
        element_type = args[0]
        id_arg: ID | None = next((arg for arg in args if isinstance(arg, ID)), None)

    elif issubclass(annotation, Element):
        element_type = annotation
        try:
            element_instance = element_type()  # type: ignore
            id_arg = ID(id=element_instance.id)
        except ValidationError:
            id_arg = None

    else:
        element_type = None
        id_arg = None

    if id_arg is None or element_type is None or not issubclass(element_type, Element):
        raise ValueError(f"element: {arg_name} is not sufficiently defined")

    return FunctionInput(
        arg_name=arg_name,
        element_type=element_type,
        element_id=id_arg.id,
    )


def get_function_inputs(func_signature: Signature) -> list[FunctionInput]:
    function_inputs: list[FunctionInput] = []
    for arg_name, arg in func_signature.parameters.items():
        function_inputs.append(
            build_function_input(arg_name=arg_name, annotation=arg.annotation)
        )

    return function_inputs
