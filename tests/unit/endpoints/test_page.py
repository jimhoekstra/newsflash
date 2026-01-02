from pytest import raises

from newsflash.widgets.widgets import Widget


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
    widget = DummyWidgetC()
    widget._build_hx_include()

    assert isinstance(widget.hx_include, list)
    assert len(widget.hx_include) == 2
    assert "#widget-a" in widget.hx_include
    assert "#widget-b" in widget.hx_include


class DummyWidgetD(Widget):
    id: str = "widget-d"

    _callback_fn_name: str = "dummy_callback_no_inputs"

    def dummy_callback_no_inputs(self) -> list[Widget]: ...


def test_build_hx_include_no_inputs():
    widget = DummyWidgetD()
    widget._build_hx_include()

    assert isinstance(widget.hx_include, list)
    assert len(widget.hx_include) == 0


class DummyWidgetE(Widget):
    id: str = "widget-e"

    _callback_fn_name: str = "dummy_callback_illegal_inputs"

    def dummy_callback_illegal_inputs(
        self,
        not_a_widget: float,
    ) -> list[Widget]: ...


def test_build_hx_include_illegal_inputs():
    widget = DummyWidgetE()

    with raises(AssertionError):
        widget._build_hx_include()


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
    widget = DummyWidgetF()
    widget._build_hx_include()

    rendered_widget = widget._render_update()
    expected = "Dummy Widget F, with hx_include: #widget-a, #widget-b, #widget-c"
    assert rendered_widget == expected
