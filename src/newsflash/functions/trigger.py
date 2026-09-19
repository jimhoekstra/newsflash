from newsflash.models import Trigger

from .registry import FunctionRegistry
from .functions import get_functions_triggered_by_element, build_hx_include_string


def get_trigger_endpoint_url(trigger: Trigger, page_path: str) -> str:
    cleaned_page_path = page_path.removeprefix("/").removesuffix("/")

    trigger_prefix = "_event"
    if len(cleaned_page_path) > 0:
        return f"/{cleaned_page_path}/{trigger_prefix}/{trigger.element_id}/{trigger.trigger}"
    else:
        return f"/{trigger_prefix}/{trigger.element_id}/{trigger.trigger}"


def get_trigger_context(
    element_id: str, element_trigger_names: list[str], functions: "FunctionRegistry", page_path: str,
) -> dict[str, str | bool]:
    function_definitions_per_trigger = get_functions_triggered_by_element(
        function_registry=functions,
        element_id=element_id,
        triggers=element_trigger_names,
    )

    trigger_context: dict[str, str | bool] = {}

    for trigger_name, function_definitions in function_definitions_per_trigger.items():
        trigger = Trigger(element_id=element_id, trigger=trigger_name)
        
        trigger_context[f"{trigger_name}_endpoint_url"] = get_trigger_endpoint_url(
            trigger=trigger,
            page_path=page_path,
        )
        trigger_context[f"has_{trigger_name}_trigger"] = len(function_definitions) > 0
        trigger_context[f"{trigger_name}_hx_include"] = build_hx_include_string(
            triggered_functions=function_definitions_per_trigger[trigger_name]
        )

    return trigger_context
