from newsflash.functions.trigger import get_trigger_context


def test_get_trigger_context_simple(
    function_registry_simple
) -> None:
    result = get_trigger_context(
        element_id="dummy-button",
        element_triggers=["click"],
        functions=function_registry_simple,
    )

    assert "has_click_trigger" in result
    assert result["has_click_trigger"] == True

    assert "click_hx_include" in result
    assert result["click_hx_include"] == "#dummy-button"


def test_get_trigger_context_multiple_triggers(
    function_registry_multiple_triggers,
) -> None:
    result = get_trigger_context(
        element_id="dummy-button",
        element_triggers=["click"],
        functions=function_registry_multiple_triggers,
    )

    assert "has_click_trigger" in result
    assert result["has_click_trigger"] == True

    assert "click_hx_include" in result
    assert result["click_hx_include"] == "#dummy-button"

    result = get_trigger_context(
        element_id="dummy-input",
        element_triggers=["input"],
        functions=function_registry_multiple_triggers,
    )

    assert "has_input_trigger" in result
    assert result["has_input_trigger"] == True

    assert "input_hx_include" in result
    # hx-include is #dummy-button and not #dummy-input because the
    # button is a function input and the input isn't.
    assert result["input_hx_include"] == "#dummy-button"


def test_get_trigger_context_single_trigger_multiple_functions(
    function_registry_single_trigger_multiple_functions,
) -> None:
    result = get_trigger_context(
        element_id="dummy-button",
        element_triggers=["click"],
        functions=function_registry_single_trigger_multiple_functions,
    )

    assert "has_click_trigger" in result
    assert result["has_click_trigger"] == True

    assert "click_hx_include" in result
    # hx-include should also contain #dummy-input since it's part of the 
    # function inputs.
    assert result["click_hx_include"] == "#dummy-button, #dummy-input"
