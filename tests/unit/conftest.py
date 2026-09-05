import typing

import pytest

from newsflash.functions import FunctionRegistry
from newsflash.models import (
    FunctionDefinition,
    FunctionInputDefinition,
    Element,
)
from newsflash.elements import Button, Input


class DummyButton(Button):
    id: str = "dummy-button"
    label: str = "Dummy Button"


class DummyInput(Input):
    id: str = "dummy-input"


@pytest.fixture
def dummy_button() -> typing.Type[Button]:
    return DummyButton


@pytest.fixture
def dummy_input() -> typing.Type[Input]:
    return DummyInput


@pytest.fixture
def callback_function_a() -> typing.Callable[[DummyButton], typing.Iterable[Element]]:
    def fn(dummy_button: DummyButton) -> typing.Iterable[Element]:
        yield dummy_button

    return fn


@pytest.fixture
def callback_function_a_input_definitions() -> list[FunctionInputDefinition]:
    return [
        FunctionInputDefinition(
            arg_name="dummy_button",
            element_type=DummyButton,
            element_id=DummyButton().id,
        )
    ]


@pytest.fixture
def callback_function_b() -> typing.Callable[
    [DummyButton, DummyInput], typing.Iterable[Element]
]:
    def fn(
        dummy_button: DummyButton, dummy_input: DummyInput
    ) -> typing.Iterable[Element]:
        yield dummy_button
        yield dummy_input

    return fn


@pytest.fixture
def callback_function_b_input_definitions() -> list[FunctionInputDefinition]:
    return [
        FunctionInputDefinition(
            arg_name="dummy_button",
            element_type=DummyButton,
            element_id=DummyButton().id,
        ),
        FunctionInputDefinition(
            arg_name="dummy_input",
            element_type=DummyInput,
            element_id=DummyInput().id,
        ),
    ]


@pytest.fixture
def function_definitions_simple(
    dummy_button,
    callback_function_a_input_definitions,
) -> list[FunctionDefinition]:
    function_definitions = [
        FunctionDefinition(
            func=callback_function_a,
            triggers=[dummy_button().click()],
            inputs=callback_function_a_input_definitions,
        )
    ]

    return function_definitions


@pytest.fixture
def function_definitions_multiple_triggers(
    dummy_button,
    dummy_input,
    callback_function_a_input_definitions,
) -> list[FunctionDefinition]:
    function_definitions = [
        FunctionDefinition(
            func=callback_function_a,
            triggers=[dummy_button().click(), dummy_input().input()],
            inputs=callback_function_a_input_definitions,
        )
    ]

    return function_definitions


@pytest.fixture
def function_definitions_single_trigger_multiple_functions(
    dummy_button,
    callback_function_a_input_definitions,
    callback_function_b_input_definitions,
) -> list[FunctionDefinition]:
    function_definitions = [
        FunctionDefinition(
            func=callback_function_a,
            triggers=[dummy_button().click()],
            inputs=callback_function_a_input_definitions,
        ),
        FunctionDefinition(
            func=callback_function_b,
            triggers=[dummy_button().click()],
            inputs=callback_function_b_input_definitions,
        ),
    ]

    return function_definitions


@pytest.fixture
def function_registry_simple(
    function_definitions_simple,
) -> FunctionRegistry:
    function_registry = FunctionRegistry()
    function_registry._functions = function_definitions_simple
    return function_registry


@pytest.fixture
def function_registry_multiple_triggers(
    function_definitions_multiple_triggers,
) -> FunctionRegistry:
    function_registry = FunctionRegistry()
    function_registry._functions = function_definitions_multiple_triggers
    return function_registry


@pytest.fixture
def function_registry_single_trigger_multiple_functions(
    function_definitions_single_trigger_multiple_functions,
) -> FunctionRegistry:
    function_registry = FunctionRegistry()
    function_registry._functions = (
        function_definitions_single_trigger_multiple_functions
    )
    return function_registry
