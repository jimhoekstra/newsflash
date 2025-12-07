from typing import Type

from pytest import raises

from newsflash.endpoints.page import build_hx_include, _build_rendered_widgets
from newsflash.widgets.widgets import Widget
from newsflash.widgets.charts import Chart


class DummyWidgetA(Widget):
    id: str = "widget-a"


class DummyWidgetB(Widget):
    id: str = "widget-b"


class DummyWidgetC(Widget):
    id: str = "widget-c"

    _callback_fn_name: str = "dummy_callback"

    def dummy_callback(
        self,
        widget_a: DummyWidgetA,
        widget_b: DummyWidgetB,
    ) -> list[Widget]: ...

    def render(self) -> str:
        return f"Dummy Widget C, with hx_include: {', '.join(self.hx_include)}"


def test_build_hx_include():
    callback_fn = DummyWidgetC.dummy_callback

    result = build_hx_include(callback_fn)

    assert isinstance(result, list)
    assert len(result) == 2
    assert "#widget-a" in result
    assert "#widget-b" in result


class DummyWidgetD(Widget):
    id: str = "widget-d"

    _callback_fn_name: str = "dummy_callback_no_inputs"

    def dummy_callback_no_inputs(self) -> list[Widget]: ...


def test_build_hx_include_no_inputs():
    callback_fn = DummyWidgetD.dummy_callback_no_inputs

    result = build_hx_include(callback_fn)

    assert isinstance(result, list)
    assert len(result) == 0


class DummyWidgetE(Widget):
    id: str = "widget-e"

    _callback_fn_name: str = "dummy_callback_illegal_inputs"

    def dummy_callback_illegal_inputs(
        self,
        not_a_widget: float,
    ) -> list[Widget]: ...


def test_build_hx_include_illegal_inputs():
    callback_fn = DummyWidgetE.dummy_callback_illegal_inputs

    with raises(AssertionError):
        build_hx_include(callback_fn)


class DummyWidgetF(Widget):
    id: str = "widget-f"

    _callback_fn_name: str = "dummy_callback"

    def dummy_callback(
        self,
        widget_a: DummyWidgetA,
        widget_b: DummyWidgetB,
        widget_c: DummyWidgetC,
    ) -> list[Widget]: ...

    def render(self) -> str:
        return f"Dummy Widget F, with hx_include: {', '.join(self.hx_include)}"


def test_build_rendered_widgets():
    widgets: list[Type[Widget]] = [DummyWidgetF]

    rendered_widgets = _build_rendered_widgets(widgets)
    expected = {
        "DummyWidgetF": "Dummy Widget F, with hx_include: #widget-a, #widget-b, #widget-c"
    }
    assert rendered_widgets == expected


def test_build_rendered_widgets_multiple():
    widgets: list[Type[Widget]] = [DummyWidgetC, DummyWidgetF]

    rendered_widgets = _build_rendered_widgets(widgets)
    expected = {
        "DummyWidgetC": "Dummy Widget C, with hx_include: #widget-a, #widget-b",
        "DummyWidgetF": "Dummy Widget F, with hx_include: #widget-a, #widget-b, #widget-c",
    }
    assert rendered_widgets == expected


class DummyChartWidget(Chart):
    id: str = "chart-widget"

    def on_load(
        self,
        widget_a: DummyWidgetA,
    ) -> list[Widget]: ...

    def render(self) -> str: ...

    def render_container(self) -> str:
        return f"Chart Widget Container, with hx_include: {', '.join(self.hx_include)}"


def test_build_rendered_widgets_chart():
    widgets: list[Type[Widget]] = [DummyChartWidget]

    rendered_widgets = _build_rendered_widgets(widgets)
    expected = {
        "DummyChartWidget": "Chart Widget Container, with hx_include: #widget-a"
    }
    assert rendered_widgets == expected
