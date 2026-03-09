from pathlib import Path

from pytest import fixture, raises

from newsflash import App, Page
from newsflash.widgets.widgets import Widget


class DummyWidgetA(Widget):
    id: str = "widget_a"


class DummyWidgetB(Widget):
    id: str = "widget_b"


class DummyWidgetC(Widget):
    id: str = "widget_c"


class DummyPage(Page):
    id: str = "test-page"
    path: str = "/test-page"
    title: str = "Test Page"
    template: tuple[str, str] = ("templates", "test_page.html")

    def compose(self) -> list[Widget]:
        return [DummyWidgetA(), DummyWidgetB()]


class DummyPageSameWidget(Page):
    id: str = "test-page"
    path: str = "/test-page"
    title: str = "Test Page"
    template: tuple[str, str] = ("templates", "test_page.html")

    def compose(self) -> list[Widget]:
        return [DummyWidgetA(), DummyWidgetA(id="widget_a_2")]


# @fixture
# def test_page() -> Page:
#     return Page(
#         id="test-page",
#         path="/test-page",
#         title="Test Page",
#         template=("templates", "test_page.html"),
#         children=[DummyWidgetA(), DummyWidgetB()],
#     )


@fixture
def test_app() -> App:
    test_page = DummyPage()
    app = App(
        pages=[test_page],
        template_folders=[("templates", Path.cwd() / "dummy" / "path")],
    )
    return app


@fixture
def test_app_same_widget() -> App:
    test_page = DummyPageSameWidget()
    app = App(
        pages=[test_page],
        template_folders=[("templates", Path.cwd() / "dummy" / "path")],
    )
    return app


def test_get_widget_by_type(
    test_app: App,
):
    widget_a = test_app.get_widget(
        path="/test-page",
        type=DummyWidgetA,
    )
    assert isinstance(widget_a, DummyWidgetA)
    assert widget_a.id == "widget_a"

    widget_b = test_app.get_widget(path="/test-page", type=DummyWidgetB)
    assert isinstance(widget_b, DummyWidgetB)
    assert widget_b.id == "widget_b"


def test_query_one_with_id(
    test_app: App,
):
    widget_a = test_app.get_widget(
        path="/test-page",
        type=Widget,
        id="widget_a",
    )
    assert isinstance(widget_a, DummyWidgetA)
    assert widget_a.id == "widget_a"


def test_query_one_multiple_found(
    test_app_same_widget: App,
):
    test_app_same_widget.pages["/test-page"].children.append(
        DummyWidgetA(id="widget_a_2")
    )

    with raises(ValueError) as e:
        test_app_same_widget.get_widget(
            path="/test-page",
            type=DummyWidgetA,
        )

    assert "specify an id" in str(e.value).lower()


def test_query_one_not_found(
    test_app: App,
):
    with raises(ValueError) as e:
        test_app.get_widget(
            path="/test-page",
            type=DummyWidgetC,
        )

    assert "no widgets" in str(e.value).lower()
