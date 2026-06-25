from typing import Iterable, Any

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from starlette.datastructures import FormData

from newsflash.elements import Element, FunctionRegistry, FunctionDefinition
from newsflash.templates import template_registry


def collect_function_inputs(
    fn: FunctionDefinition, values: FormData
) -> dict[str, Element]:
    function_inputs: dict[str, Element] = {}

    for function_input in fn.inputs:
        input_type = function_input.element_type

        input_values: dict[str, Any] = {
            "id": function_input.element_id,
        }

        for k, v in values.items():
            input_id, input_parameter = k.split("--")
            if input_id == function_input.element_id:
                input_values[input_parameter] = v

        input_element = input_type.model_validate(input_values)
        function_inputs[function_input.arg_name] = input_element

    return function_inputs


def build_function_endpoint(fn: FunctionDefinition, fn_registry: FunctionRegistry):

    async def function_endpoint(request: Request) -> HTMLResponse:
        body = await request.form()

        fn_inputs = collect_function_inputs(
            fn=fn,
            values=body,
        )

        fn_outputs: Iterable[Element] = fn.func(**fn_inputs)

        rendered_outputs: list[str] = [
            fn_output.render(functions=fn_registry, hx_swap_oob="true")
            for fn_output in fn_outputs
        ]

        return HTMLResponse(content="\n".join(rendered_outputs), status_code=200)

    return function_endpoint


class NewsflashApp(FastAPI):
    function_registry: FunctionRegistry
    template_dir_name: str = "newsflash-pages"
    template_name: str = "main.html"

    def __init__(self, functions: FunctionRegistry) -> None:
        super().__init__()
        self.function_registry = functions
        self.register_root_page()
        self.register_function_endpoints()

    def register_root_page(self) -> None:
        def root_page(request: Request) -> Response:
            return self.render(request=request)

        self.add_api_route(path="/", endpoint=root_page, methods=["GET"])

    def register_function_endpoints(self) -> None:

        for fn in self.function_registry.functions:
            for trigger in fn.triggers:
                self.add_api_route(
                    path=f"/{trigger.element.name}/{trigger.element.id}/{trigger.trigger}",
                    endpoint=build_function_endpoint(
                        fn=fn, fn_registry=self.function_registry
                    ),
                    methods=["POST"],
                )

    def render(self, request: Request) -> Response:
        elements = list(self.compose())

        return template_registry.get_jinja2_templates(
            dir_name=self.template_dir_name,
        ).TemplateResponse(
            request=request,
            name=self.template_name,
            context={
                "elements": {
                    element.id: element.render(
                        functions=self.function_registry, hx_swap_oob=None
                    )
                    for element in elements
                }
            },
        )

    def compose(self) -> Iterable["Element"]:
        yield from ()
