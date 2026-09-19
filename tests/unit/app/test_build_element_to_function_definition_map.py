from newsflash.app.app import _build_element_to_function_definitions_map


def test_build_element_to_function_definition_map(
    function_definitions_simple,
) -> None:
    result = _build_element_to_function_definitions_map(
        page_path="/page-url", function_definitions=function_definitions_simple
    )

    assert list(result.keys()) == ["/page-url/_event/dummy-button/click"]
    assert list(result.values()) == [function_definitions_simple]


def test_multiple_triggers_for_single_function(
    function_definitions_multiple_triggers,
) -> None:
    result = _build_element_to_function_definitions_map(
        page_path="/page-url",
        function_definitions=function_definitions_multiple_triggers,
    )

    assert len(result) == 2

    assert "/page-url/_event/dummy-button/click" in result
    assert (
        result["/page-url/_event/dummy-button/click"]
        == function_definitions_multiple_triggers
    )

    assert "/page-url/_event/dummy-input/input" in result
    assert (
        result["/page-url/_event/dummy-input/input"]
        == function_definitions_multiple_triggers
    )


def test_single_trigger_for_multiple_callback_functions(
    function_definitions_single_trigger_multiple_functions,
) -> None:
    result = _build_element_to_function_definitions_map(
        page_path="/page-url",
        function_definitions=function_definitions_single_trigger_multiple_functions,
    )

    assert len(result) == 1

    assert list(result.keys()) == ["/page-url/_event/dummy-button/click"]
    assert list(result.values()) == [
        function_definitions_single_trigger_multiple_functions
    ]
