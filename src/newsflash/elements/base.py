import typing
from inspect import Signature, signature
from functools import wraps

from pydantic import BaseModel

from newsflash.templates import template_registry


class Element(BaseModel):
    id: str
    name: str
    template_dir_name: str
    template_name: str

    children: list["Element"] = []

    def get_trigger_context(
        self, functions: "FunctionRegistry"
    ) -> dict[str, str | bool]:
        function_definitions = get_functions_triggered_by_element(
            function_registry=functions,
            element_id=self.id,
        )

        if len(function_definitions) == 0:
            return {"is_trigger": False}

        hx_include_string = build_hx_include_string(
            triggered_functions=function_definitions
        )

        return {
            "is_trigger": True,
            "hx_include": hx_include_string,
        }

    def render(self, functions: "FunctionRegistry", hx_swap_oob: str | None) -> str:
        template = template_registry.get_template(
            dir_name=self.template_dir_name,
            template_file_name=self.template_name,
        )

        trigger_context = self.get_trigger_context(functions=functions)

        return template.render(
            {
                **self.model_dump(exclude={"_children"}),
                "hx_swap_oob": hx_swap_oob,
                "elements": {
                    element.id: element.render(functions=functions, hx_swap_oob=None)
                    for element in self.compose()
                },
                **trigger_context,
            }
        )

    def compose(self) -> typing.Iterable["Element"]:
        yield from self.children


class Trigger(BaseModel):
    element: Element
    trigger: str


class FunctionInput(BaseModel):
    arg_name: str
    element_type: typing.Type[Element]
    element_id: str


def build_function_input(arg_name: str, annotation: typing.Any) -> FunctionInput:
    origin = typing.get_origin(annotation)
    if origin != typing.Annotated:
        raise ValueError("type is not annotated")

    args = typing.get_args(annotation)
    id_arg = args[1]

    return FunctionInput(
        arg_name=arg_name,
        element_type=args[0],
        element_id=id_arg,
    )


def get_function_inputs(func_signature: Signature) -> list[FunctionInput]:
    function_inputs: list[FunctionInput] = []
    for arg_name, arg in func_signature.parameters.items():
        function_inputs.append(
            build_function_input(arg_name=arg_name, annotation=arg.annotation)
        )

    return function_inputs


class FunctionDefinition(BaseModel):
    func: typing.Callable[..., typing.Any]
    triggers: list[Trigger]
    inputs: list[FunctionInput]


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


def get_functions_triggered_by_element(
    function_registry: FunctionRegistry, element_id: str
) -> list[FunctionDefinition]:
    function_definitions: list[FunctionDefinition] = []

    for func in function_registry.functions:
        for trigger in func.triggers:
            if trigger.element.id == element_id:
                function_definitions.append(func)

    return function_definitions


def build_hx_include_string(triggered_functions: list[FunctionDefinition]) -> str:
    element_ids: list[str] = []

    for func in triggered_functions:
        for func_input in func.inputs:
            element_ids.append(f"#{func_input.element_id}")

    return ", ".join(element_ids)
