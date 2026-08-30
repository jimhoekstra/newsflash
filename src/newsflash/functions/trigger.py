from .registry import FunctionRegistry
from .functions import get_functions_triggered_by_element, build_hx_include_string


def get_trigger_context(
    element_id: str, element_triggers: list[str], functions: "FunctionRegistry"
) -> dict[str, str | bool]:
    function_definitions_per_trigger = get_functions_triggered_by_element(
        function_registry=functions,
        element_id=element_id,
        triggers=element_triggers,
    )

    trigger_context: dict[str, str | bool] = {}

    for trigger, function_definitions in function_definitions_per_trigger.items():
        trigger_context[f"has_{trigger}_trigger"] = len(function_definitions) > 0
        trigger_context[f"{trigger}_hx_include"] = build_hx_include_string(
            triggered_functions=function_definitions_per_trigger[trigger]
        )

    return trigger_context
