from newsflash.endpoints.parsers import (
    _parse_trigger_element_id,
    _parse_url_path,
    _parse_chart_dimensions,
    parse_request_values,
)
from starlette.datastructures import Headers, FormData


def test_parse_trigger_element_id():
    headers = Headers(
        {
            "hx-trigger": "my-button-id",
        }
    )

    trigger_element_id = _parse_trigger_element_id(headers)
    assert trigger_element_id == "my-button-id"


def test_parse_url_path():
    headers = Headers(
        {
            "hx-current-url": "https://example.com/some/path?query=param",
        }
    )

    url_path = _parse_url_path(headers)
    assert url_path == "/some/path"


def test_parse_chart_dimensions():
    body = FormData(
        {
            "dimensions": '{"chart-width": "800", "chart-height": "600"}',
        }
    )

    dimensions = _parse_chart_dimensions(body)
    assert dimensions == {"chart-width": 800.0, "chart-height": 600.0}


def test_parse_multiple_chart_dimensions():
    body = FormData(
        {
            "dimensions": '{"chart-1-width": "800", "chart-1-height": "600", '
            '"chart-2-width": "400", "chart-2-height": "300"}',
        }
    )

    dimensions = _parse_chart_dimensions(body)
    assert dimensions == {
        "chart-1-width": 800.0,
        "chart-1-height": 600.0,
        "chart-2-width": 400.0,
        "chart-2-height": 300.0,
    }


def test_parse_chart_dimensions_no_dimensions():
    body = FormData({})

    dimensions = _parse_chart_dimensions(body)
    assert dimensions == {}


def test_parse_request_values():
    body = FormData(
        {
            "input-1-value": "some text",
            "select-1-value": "option-2",
            "dimensions": '{"chart-width": "800", "chart-height": "600"}',
        }
    )
    headers = Headers(
        {
            "hx-trigger": "input-1",
            "hx-current-url": "https://example.com/dashboard/view?query=value",
        }
    )

    request_values = parse_request_values(body, headers)

    assert request_values.trigger_element_id == "input-1"
    assert request_values.url_path == "/dashboard/view"
    assert request_values.widget_attributes == {
        "input-1-value": "some text",
        "select-1-value": "option-2",
        "chart-width": 800.0,
        "chart-height": 600.0,
    }
