from typing import Type

from pytest import fixture, raises

from newsflash import App, Page
from newsflash.widgets.widgets import Widget


@fixture
def test_widget_a() -> Type[Widget]:
    class TestWidgetA(Widget):
        id: str = "widget_a"

    return TestWidgetA


@fixture
def test_widget_b() -> Type[Widget]:
    class TestWidgetB(Widget):
        id: str = "widget_b"

    return TestWidgetB


@fixture
def test_widget_c() -> Type[Widget]:
    class TestWidgetC(Widget):
        id: str = "widget_c"

    return TestWidgetC


@fixture
def test_page(test_widget_a: Type[Widget], test_widget_b: Type[Widget]) -> Page:
    return Page(
        path="/test-page",
        title="Test Page",
        template="test-page.html",
        widgets=[test_widget_a, test_widget_b],
    )


@fixture
def test_app(test_page: Page) -> App:
    app = App(pages=[test_page])
    return app


def test_query_one(
    test_app: App,
    test_widget_a: Type[Widget],
    test_widget_b: Type[Widget],
):
    widget_a = test_app.query_one("/test-page", test_widget_a)
    assert widget_a is test_widget_a

    widget_b = test_app.query_one("/test-page", test_widget_b, id="widget_b")
    assert widget_b is test_widget_b


def test_query_one_with_id(
    test_app: App,
    test_widget_a: Type[Widget],
):
    widget_a = test_app.query_one("/test-page", test_widget_a, id="widget_a")
    assert widget_a is test_widget_a


def test_query_one_multiple_found(
    test_app: App,
    test_widget_a: Type[Widget],
):
    # Add another instance of test_widget_a to the page to simulate
    # multiple widgets of the same type. #TODO: update once having
    # multiple widgets of the same type but different ID is actually
    # possible.
    test_app.pages["/test-page"].widgets.append(test_widget_a)

    with raises(ValueError) as e:
        test_app.query_one("/test-page", test_widget_a)

    assert "please specify an id" in str(e.value).lower()


def test_query_one_not_found(
    test_app: App,
    test_widget_c: Type[Widget],
):
    with raises(ValueError) as e:
        test_app.query_one("/test-page", test_widget_c)

    assert "not found" in str(e.value).lower()
