import typing

import pytest

from newsflash.models import (
    FunctionDefinition,
    FunctionInputDefinition,
    Element,
)
from newsflash.elements import Button, Input

from newsflash.app.app import _build_element_to_function_definitions_map


class DummyButton(Button):
    id: str = "dummy-button"
    label: str = "Dummy Button"


class DummyInput(Input):
    id: str = "dummy-input"


def callback_function_a(dummy_button: DummyButton) -> typing.Iterable[Element]: ...


@pytest.fixture
def callback_function_a_input_definitions() -> list[FunctionInputDefinition]:
    return [
        FunctionInputDefinition(
            arg_name="dummy_button",
            element_type=DummyButton,
            element_id=DummyButton().id,
        )
    ]


def callback_function_b(
    dummy_button: DummyButton, dummy_input: DummyInput
) -> typing.Iterable[Element]: ...


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


def test_build_element_to_function_definition_map(
    callback_function_a_input_definitions: list[FunctionInputDefinition],
) -> None:
    test_trigger = DummyButton().click()

    function_definitions = [
        FunctionDefinition(
            func=callback_function_a,
            triggers=[test_trigger],
            inputs=callback_function_a_input_definitions,
        )
    ]

    result = _build_element_to_function_definitions_map(
        function_definitions=function_definitions
    )

    assert list(result.keys()) == ["/button/dummy-button/click"]
    assert list(result.values()) == [function_definitions]


def test_multiple_triggers_for_single_function(
    callback_function_a_input_definitions: list[FunctionInputDefinition],
) -> None:
    button_trigger = DummyButton().click()
    input_trigger = DummyInput().input()

    function_definitions = [
        FunctionDefinition(
            func=callback_function_a,
            triggers=[button_trigger, input_trigger],
            inputs=callback_function_a_input_definitions,
        )
    ]

    result = _build_element_to_function_definitions_map(
        function_definitions=function_definitions
    )

    assert len(result) == 2

    assert "/button/dummy-button/click" in result
    assert result["/button/dummy-button/click"] == function_definitions

    assert "/input/dummy-input/input" in result
    assert result["/input/dummy-input/input"] == function_definitions


def test_single_trigger_for_multiple_callback_functions(
    callback_function_a_input_definitions: list[FunctionInputDefinition],
    callback_function_b_input_definitions: list[FunctionInputDefinition],
) -> None:
    button_trigger = DummyButton().click()

    function_definitions = [
        FunctionDefinition(
            func=callback_function_a,
            triggers=[button_trigger],
            inputs=callback_function_a_input_definitions,
        ),
        FunctionDefinition(
            func=callback_function_b,
            triggers=[button_trigger],
            inputs=callback_function_b_input_definitions,
        ),
    ]

    result = _build_element_to_function_definitions_map(
        function_definitions=function_definitions
    )

    assert len(result) == 1

    assert list(result.keys()) == ["/button/dummy-button/click"]
    assert list(result.values()) == [function_definitions]
