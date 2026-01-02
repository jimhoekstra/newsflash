from typing import Any

from pytest import raises

from newsflash.endpoints.parsers import RequestValues
from newsflash.widgets.widgets import Widget


class DummyWidget(Widget):
    id: str = "dummy-widget"
    test_value_a: str = ""
    test_value_b: float = 0.0

    _values_from_request: list[str] = ["test_value_a", "test_value_b"]
    _callback_fn_name: str = "dummy_callback"

    def dummy_callback(self) -> list[Widget]: ...


def test_widget_set_value_from_request():
    dummy_widget = DummyWidget()

    request_data: dict[str, Any] = {
        "dummy-widget-test_value_a": "Hello, World!",
        "dummy-widget-test_value_b": 3.14,
    }

    dummy_widget._set_value_from_request("test_value_a", request_data)
    dummy_widget._set_value_from_request("test_value_b", request_data)

    assert dummy_widget.test_value_a == "Hello, World!"
    assert dummy_widget.test_value_b == 3.14


def test_widget_set_value_no_attribute():
    dummy_widget = DummyWidget()

    request_data: dict[str, Any] = {
        "dummy-widget-test_value_a": "Hello, World!",
        "dummy-widget-test_value_c": 3.14,
    }

    with raises(AssertionError) as e:
        dummy_widget._set_value_from_request("test_value_c", request_data)

    assert str(e.value) == "Widget has no attribute 'test_value_c'"


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
    dummy_widget = DummyWidget()

    request_data: dict[str, Any] = {
        "dummy-widget-test_value_a": 100,
        "dummy-widget-test_value_b": 3.14,
    }

    with raises(AssertionError) as e:
        dummy_widget._set_value_from_request("test_value_a", request_data)

    assert (
        str(e.value)
        == "Expected type <class 'str'> for key 'test_value_a', got <class 'int'>"
    )


def test_widget_set_values_from_request():
    dummy_widget = DummyWidget()

    request_data: dict[str, Any] = {
        "dummy-widget-test_value_a": "Hello, World!",
        "dummy-widget-test_value_b": 3.14,
    }

    request_values = RequestValues(
        trigger_element_id="some-widget",
        url_path="/dummy",
        widget_attributes=request_data,
    )

    dummy_widget._set_values_from_request(request_values)

    assert dummy_widget.test_value_a == "Hello, World!"
    assert dummy_widget.test_value_b == 3.14


def test_widget_factory():
    request_data: dict[str, Any] = {
        "dummy-widget-test_value_a": "Hello, World!",
        "dummy-widget-test_value_b": 3.14,
    }

    request_values = RequestValues(
        trigger_element_id="some-widget",
        url_path="/dummy",
        widget_attributes=request_data,
    )

    widget = DummyWidget(request_values=request_values)
    widget._post_init()

    assert isinstance(widget, DummyWidget)
    assert widget.test_value_a == "Hello, World!"
    assert widget.test_value_b == 3.14


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

    no_callback_widget = NoCallbackWidget()

    with raises(AssertionError) as e:
        no_callback_widget._get_callback_fn()

    assert str(e.value) == "Widget has no callback function 'non_existent_callback'"
