from pytest import raises

from newsflash.widgets import Select, Input, TextArea, Button


def test_select_init_with_selected():
    select_widget = Select(
        options=["Option 1", "Option 2", "Option 3"], selected="Option 2"
    )

    assert select_widget.selected == "Option 2"


def test_select_init_default():
    # Test with default function
    def default_option():
        return "Option 2"

    select_widget = Select(
        options=["Option 1", "Option 2", "Option 3"], default=default_option
    )

    assert select_widget.selected == "Option 2"


def test_select_init_no_default():
    # Test without default function
    select_widget = Select(options=["Option 1", "Option 2", "Option 3"])

    assert (
        select_widget.selected == "Option 1"
    )  # First option should be selected by default


def test_select_no_options():
    with raises(ValueError, match="Select widget has no options to select from."):
        Select(options=[])


def test_select_default_on_select():
    select_widget = Select(options=["Option 1", "Option 2", "Option 3"])

    # Simulate selecting an option
    select_widget.selected = "Option 2"
    result = select_widget.on_select()

    assert isinstance(result, list)  # Ensure it returns a list
    assert len(result) == 0  # No widgets should be returned by default


def test_input_default_on_input():
    input_widget = Input(value="Test input")

    # Simulate input event
    result = input_widget.on_input()

    assert isinstance(result, list)  # Ensure it returns a list
    assert len(result) == 0  # No widgets should be returned by default


def test_textarea_default_on_input():
    textarea_widget = TextArea(value="Test textarea", rows=5)

    # Simulate input event
    result = textarea_widget.on_input()

    assert isinstance(result, list)  # Ensure it returns a list
    assert len(result) == 0  # No widgets should be returned by default


def test_button_default_on_click():
    button_widget = Button(label="Submit")

    # Simulate button click
    result = button_widget.on_click()

    assert isinstance(result, list)  # Ensure it returns a list
    assert len(result) == 0  # No widgets should be returned by default
