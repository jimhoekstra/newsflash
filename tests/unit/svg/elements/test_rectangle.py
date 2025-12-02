from pytest import fixture

from newsflash.svg.elements import (
    Rectangle,
    build_rectangle,
    build_rectangle_from_bottom_center,
    build_background_rectangle,
)
from newsflash.svg.utils import Point
from newsflash.svg.box import Box


def test_build_rectangle():
    rect = build_rectangle(
        top_left=Point(x=10, y=20),
        width=200,
        height=100,
        rounded=5,
        classes=["test-rect"],
    )

    assert rect.top_left.x == 10
    assert rect.top_left.y == 20
    assert rect.width == 200
    assert rect.height == 100
    assert rect.rounded == 5
    assert "test-rect" in rect.classes


def test_build_rectangle_with_box():
    box = Box(
        top=0,
        right=200,
        bottom=200,
        left=0,
    )

    rect = build_rectangle(
        top_left=Point(x=0.5, y=0.5),
        width=0.5,
        height=0.5,
        rounded=5,
        classes=["boxed-rect"],
        box=box,
    )

    assert rect.top_left.x == 100  # 0.5 scaled to box width 200
    assert rect.top_left.y == 100  # 0.5 scaled to box height 200
    assert rect.width == 100  # 0.5 scaled to box width 200
    assert rect.height == 100  # 0.5 scaled to box height 200
    assert rect.rounded == 5
    assert "boxed-rect" in rect.classes


def test_build_rectangle_from_bottom_center():
    rect = build_rectangle_from_bottom_center(
        bottom_center=Point(x=150, y=300),
        width=200,
        height=100,
        rounded=10,
        classes=["bottom-center-rect"],
    )

    assert rect.top_left.x == 50  # 150 - 200/2
    assert rect.top_left.y == 200  # 300 - 100
    assert rect.width == 200
    assert rect.height == 100
    assert rect.rounded == 10
    assert "bottom-center-rect" in rect.classes


def test_build_rectangle_from_bottom_center_with_box():
    box = Box(
        top=0,
        right=400,
        bottom=400,
        left=0,
    )

    rect = build_rectangle_from_bottom_center(
        bottom_center=Point(x=0.75, y=0.75),
        width=0.5,
        height=0.25,
        rounded=10,
        classes=["boxed-bottom-center-rect"],
        box=box,
    )

    assert rect.top_left.x == 200  # 300 - 200/2
    assert rect.top_left.y == 200  # 300 - 100
    assert rect.width == 200  # 0.5 scaled to box width 400
    assert rect.height == 100  # 0.25 scaled to box height 400
    assert rect.rounded == 10
    assert "boxed-bottom-center-rect" in rect.classes


def test_build_background_rectangle():
    box = Box(
        top=0,
        right=800,
        bottom=600,
        left=0,
    )
    rect = build_background_rectangle(
        box=box,
        classes=["background-rect"],
    )

    assert rect.top_left.x == 0
    assert rect.top_left.y == 0
    assert rect.width == 800
    assert rect.height == 600
    assert rect.rounded == 0
    assert "background-rect" in rect.classes


def test_build_background_rectangle_with_padding():
    box = Box(
        top=0,
        right=800,
        bottom=600,
        left=0,
        padding_top=0.05,
        padding_right=0.05,
        padding_bottom=0.05,
        padding_left=0.05,
    )
    rect = build_background_rectangle(
        box=box,
        classes=["padded-background-rect"],
    )

    assert rect.top_left.x == 0
    assert rect.top_left.y == 0
    assert rect.width == 800
    assert rect.height == 600
    assert rect.rounded == 0
    assert "padded-background-rect" in rect.classes


@fixture
def rect1() -> Rectangle:
    return Rectangle(
        top_left=Point(x=10, y=20),
        width=200,
        height=100,
        rounded=5,
        classes=["test-rect"],
    )


def test_top(rect1: Rectangle):
    assert rect1.top == 20


def test_right(rect1: Rectangle):
    assert rect1.right == 210


def test_bottom(rect1: Rectangle):
    assert rect1.bottom == 120


def test_left(rect1: Rectangle):
    assert rect1.left == 10


def test_render():
    rect = Rectangle(
        top_left=Point(x=10, y=20),
        width=200,
        height=100,
        classes=["test-rect"],
        styles=["test-style: value;"],
        attributes={"data-test": "rectangle"},
    )

    result = rect.render()
    expected = """<rect 
    class="test-rect" 
    x="10.0" 
    y="20.0" 
    width="200.0" 
    height="100.0" 
    rx="0.0" 
    ry="0.0" 
    style="test-style: value;"
    data-test="rectangle"
/>"""

    assert result == expected
