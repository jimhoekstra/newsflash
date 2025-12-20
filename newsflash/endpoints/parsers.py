import json
from typing import Any
from urllib.parse import urlparse

from starlette.datastructures import FormData, Headers
from pydantic import BaseModel


class RequestValues(BaseModel):
    trigger_element_id: str
    url_path: str
    widget_attributes: dict[str, Any]


def _parse_trigger_element_id(headers: Headers) -> str:
    hx_trigger = headers["hx-trigger"]
    return hx_trigger


def _parse_url_path(headers: Headers) -> str:
    current_url = headers["hx-current-url"]
    parsed_url = urlparse(current_url)
    return parsed_url.path


def _parse_chart_dimensions(body: FormData) -> dict[str, float]:
    dimensions = body.get("dimensions")
    if not isinstance(dimensions, str):
        return {}

    dimensions_dict: dict[str, Any] = json.loads(dimensions)
    dimensions_dict = {k: float(v) for k, v in dimensions_dict.items()}

    return dimensions_dict


def parse_request_values(body: FormData, headers: Headers) -> RequestValues:
    trigger_element_id = _parse_trigger_element_id(headers)
    url_path = _parse_url_path(headers)

    widget_attributes: dict[str, Any] = {}

    for key, value in body.items():
        if key != "dimensions":
            assert isinstance(value, str)
            widget_attributes[key] = value

    chart_dimensions = _parse_chart_dimensions(body)
    widget_attributes.update(chart_dimensions)

    return RequestValues(
        trigger_element_id=trigger_element_id,
        url_path=url_path,
        widget_attributes=widget_attributes,
    )
