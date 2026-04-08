from typing import Any, Annotated

from pytest import raises
from pydantic import ValidationError

from newsflash.widgets.widgets import Widget, BodyParam


class DummyWidget(Widget):
    id: str = "dummy-widget"
    test_value_a: Annotated[str, BodyParam()] = ""
    test_value_b: Annotated[float, BodyParam()] = 0.0

    _values_from_request: list[str] = ["test_value_a", "test_value_b"]
    _callback_fn_name: str = "dummy_callback"

    def dummy_callback(self) -> list[Widget]: ...


def test_widget_set_value_from_request():
    body_params: dict[str, Any] = {
        "dummy-widget-test_value_a": "Hello, World!",
        "dummy-widget-test_value_b": 3.14,
    }
    dummy_widget = DummyWidget().initialize(
        body_params=body_params,
    )

    assert dummy_widget.test_value_a == "Hello, World!"
    assert dummy_widget.test_value_b == 3.14


def test_widget_set_value_no_attribute():
    body_params: dict[str, Any] = {
        "dummy-widget-test_value_a": "Hello, World!",
        "dummy-widget-test_value_c": 3.14,
    }
    dummy_widget = DummyWidget().initialize(
        body_params=body_params,
    )

    assert dummy_widget.test_value_a == "Hello, World!"
    assert dummy_widget.test_value_b == 0.0
    assert not hasattr(dummy_widget, "test_value_c")


# TODO: design expected behavior for missing keys
# def test_widget_set_value_from_request_missing_key():
#     dummy_widget = DummyWidget()
#     request_data: dict[str, Any] = {
#         "dummy-widget-test_value_a": "Hello, World!",
#         # "dummy-widget-test_value_b" is missing
#     }

#     with raises(AssertionError) as e:
#         dummy_widget._set_value_from_request("test_value_b", request_data)

#     assert str(e.value) == "No value provided for key 'test_value_b'"


def test_widget_set_value_wrong_type():
    body_params: dict[str, Any] = {
        "dummy-widget-test_value_a": 100,
        "dummy-widget-test_value_b": 3.14,
    }

    with raises(ValidationError):
        DummyWidget().initialize(
            body_params=body_params,
        )


def test_get_widget_callback_fn():
    dummy_widget = DummyWidget()
    callback_fn = dummy_widget._get_callback_fn()
    assert callback_fn == dummy_widget.dummy_callback


def test_get_widget_callback_none():
    class NoCallbackWidget(Widget):
        id: str = "no-callback-widget"
        _callback_fn_name: str | None = None

    no_callback_widget = NoCallbackWidget()

    callback_fn = no_callback_widget._get_callback_fn()
    assert callback_fn is None


def test_get_widget_callback_fn_no_callback():
    class NoCallbackWidget(Widget):
        id: str = "no-callback-widget"
        _callback_fn_name: str = "non_existent_callback"

    with raises(AssertionError) as e:
        NoCallbackWidget().initialize()

    assert "Widget has no callback function 'non_existent_callback'" in str(e.value)
