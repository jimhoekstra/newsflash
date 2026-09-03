from newsflash.functions.functions import get_functions_triggered_by_element


def test_get_functions_triggered_by_element(
    function_registry_simple,
    function_definitions_simple,
) -> None:
    result = get_functions_triggered_by_element(
        function_registry=function_registry_simple,
        element_id="dummy-button",
        triggers=["click"],
    )

    assert list(result.keys()) == ["click"]
    assert list(result.values()) == [
        function_definitions_simple,
    ]


def test_get_functions_triggered_by_element_second_trigger(
    function_registry_simple,
    function_definitions_simple,
) -> None:
    result = get_functions_triggered_by_element(
        function_registry=function_registry_simple,
        element_id="dummy-button",
        triggers=["click", "some-other-trigger"],
    )

    assert len(result) == 2

    assert "click" in result
    assert result["click"] == function_definitions_simple

    assert "some-other-trigger" in result
    assert result["some-other-trigger"] == []


def test_get_functions_triggered_by_button_element_multiple_triggers(
    function_registry_multiple_triggers,
    function_definitions_multiple_triggers,
) -> None:
    result = get_functions_triggered_by_element(
        function_registry=function_registry_multiple_triggers,
        element_id="dummy-button",
        triggers=["click", "input"],
    )

    assert len(result) == 2

    assert "click" in result
    assert result["click"] == function_definitions_multiple_triggers

    assert "input" in result
    # Even though the "input" event is a trigger to the function in this
    # function registry, we're only asking for the functions that are triggered
    # by the element with the "dummy-button" ID in this case.
    assert result["input"] == []


def test_get_functions_triggered_by_input_element_multiple_triggers(
    function_registry_multiple_triggers,
    function_definitions_multiple_triggers,
) -> None:
    result = get_functions_triggered_by_element(
        function_registry=function_registry_multiple_triggers,
        element_id="dummy-input",
        triggers=["click", "input"],
    )

    assert len(result) == 2

    assert "input" in result
    assert result["input"] == function_definitions_multiple_triggers

    assert "click" in result
    # Even though the "input" event is a trigger to the function in this
    # function registry, we're only asking for the functions that are triggered
    # by the element with the "dummy-button" ID in this case. This is the opposite
    # of the previous test function.
    assert result["click"] == []
