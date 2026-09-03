from newsflash.models import FunctionDefinition

from .registry import FunctionRegistry


def get_functions_triggered_by_element(
    function_registry: FunctionRegistry, element_id: str, triggers: list[str]
) -> dict[str, list[FunctionDefinition]]:
    function_definitions_per_trigger: dict[str, list[FunctionDefinition]] = {}

    for trigger in triggers:
        function_definitions: list[FunctionDefinition] = []
        for fn in function_registry._functions:
            for function_trigger in fn.triggers:
                if (
                    function_trigger.element_id == element_id
                    and function_trigger.trigger == trigger
                ):
                    function_definitions.append(fn)

        function_definitions_per_trigger[trigger] = function_definitions

    return function_definitions_per_trigger


def build_hx_include_string(triggered_functions: list[FunctionDefinition]) -> str:
    if len(triggered_functions) == 0:
        return ""

    element_ids: list[str] = []

    for function in triggered_functions:
        for function_input in function.inputs:
            element_ids.append(f"#{function_input.element_id}")

    # Sort the element IDs to make the function output deterministic and
    # easier to test
    return ", ".join(sorted(set(element_ids)))
