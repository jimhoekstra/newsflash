from .registry import FunctionRegistry
from .function_definition import FunctionDefinition


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
    element_queries: list[str] = []

    for func in triggered_functions:
        for func_input in func.inputs:
            element_queries.append(func_input.element_query)

    return ", ".join(element_queries)
