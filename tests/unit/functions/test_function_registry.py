from unittest.mock import patch

from newsflash.functions.registry import FunctionRegistry


def test_function_registry_add_callback_a(
    callback_function_a,
    callback_function_a_triggers,
    callback_function_a_input_definitions,
    function_definitions_simple,
    dummy_button,
) -> None:
    function_registry = FunctionRegistry()
    with patch(
        "newsflash.functions.registry.get_function_input_definitions",
        return_value=callback_function_a_input_definitions,
    ):
        function_registry._add(
            on=callback_function_a_triggers, function=callback_function_a
        )

    assert len(function_registry._functions) == 1
    assert (
        function_registry._functions[0].triggers
        == function_definitions_simple[0].triggers
    )
    assert (
        function_registry._functions[0].inputs == function_definitions_simple[0].inputs
    )
    # TODO: test that also the functions are the same. This is a bit tricky
    # due to how pytest deals with fixtures


def test_function_registry_add_callback_a_single_trigger(
    callback_function_a,
    callback_function_a_triggers,
    callback_function_a_input_definitions,
    function_definitions_simple,
    dummy_button,
) -> None:
    function_registry = FunctionRegistry()

    with patch(
        "newsflash.functions.registry.get_function_input_definitions",
        return_value=callback_function_a_input_definitions,
    ):
        function_registry._add(
            # The `on` argument can also take a single trigger instead of a list,
            # that's what we're testing here.
            on=callback_function_a_triggers[0],
            function=callback_function_a,
        )

    assert len(function_registry._functions) == 1
    assert (
        function_registry._functions[0].triggers
        == function_definitions_simple[0].triggers
    )
    assert (
        function_registry._functions[0].inputs == function_definitions_simple[0].inputs
    )

    inputs = dummy_button()
    function_registry._functions[0].func(inputs)
    callback_function_a.assert_called_once_with(inputs)


def test_function_registry_add_using_decorator(
    dummy_button,
    callback_function_a_triggers,
) -> None:
    function_registry = FunctionRegistry()
    function_called = False

    # Register an example callback function using the same trigger(s) as
    # for the fixture callback_function_a
    @function_registry.add(on=dummy_button().click())
    def example_callback():
        nonlocal function_called
        function_called = True
        return []

    assert len(function_registry._functions) == 1
    assert function_registry._functions[0].triggers == callback_function_a_triggers
    assert function_registry._functions[0].inputs == []

    result = function_registry._functions[0].func()
    assert result == []
    assert function_called
