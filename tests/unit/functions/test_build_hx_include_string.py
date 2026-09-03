from newsflash.functions.functions import build_hx_include_string


def test_build_hx_include_string_simple(
    function_definitions_simple
) -> None:
    result = build_hx_include_string(
        triggered_functions=function_definitions_simple,
    )

    assert result == "#dummy-button"


def test_build_hx_include_string_multiple_functions(
    function_definitions_single_trigger_multiple_functions
) -> None:
    result = build_hx_include_string(
        triggered_functions=function_definitions_single_trigger_multiple_functions
    )

    assert result == "#dummy-button, #dummy-input"


def test_build_hx_include_string_empty_list() -> None:
    result = build_hx_include_string(triggered_functions=[])
    assert result == ""
