from pytest import fixture
from unittest.mock import patch

from newsflash.svg.utils import Point
from newsflash.svg.elements import Text, build_text
from newsflash.svg.box import Box


@fixture
def text_pos() -> Point:
    return Point(x=200, y=100)


@fixture
def text_str() -> str:
    return "Test"


@fixture
def text_font_size() -> int:
    return 16


@patch("newsflash.svg.elements.text.get_text_width", return_value=100.0)
def test_build_text(get_text_width_mock, text_pos, text_str, text_font_size):
    text = build_text(
        pos=text_pos,
        text=text_str,
        font=None,  # type: ignore because get_text_width is mocked
        font_size=text_font_size,
        horizontal_align="left",
        classes=["test-class"],
        styles=["fill: black;"],
    )

    assert text.pos == text_pos
    assert text.text == text_str
    assert text.width == 100.0
    assert text.font_size == text_font_size
    assert text.classes == ["test-class"]
    assert text.styles == ["fill: black;", "font-size: 16px;"]


@patch("newsflash.svg.elements.text.get_text_width", return_value=100.0)
def test_build_text_with_box(get_text_width_mock, text_str, text_font_size):
    box = Box(
        top=0,
        right=800,
        bottom=600,
        left=0,
    )

    text = build_text(
        pos=Point(x=0.5, y=0.5),  # Relative position
        text=text_str,
        font=None,  # type: ignore because get_text_width is mocked
        font_size=text_font_size,
        horizontal_align="left",
        box=box,
    )

    assert text.pos == Point(x=400.0, y=300.0)  # Scaled to box
    assert text.text == text_str


@patch("newsflash.svg.elements.text.get_text_width", return_value=100.0)
def test_build_text_align_center(
    get_text_width_mock, text_pos, text_str, text_font_size
):
    text = build_text(
        pos=text_pos,
        text=text_str,
        font=None,  # type: ignore because get_text_width is mocked
        font_size=text_font_size,
        horizontal_align="center",
    )

    assert text.pos == Point(x=150.0, y=100)  # Adjusted for center alignment


@patch("newsflash.svg.elements.text.get_text_width", return_value=100.0)
def test_build_text_align_right(
    get_text_width_mock, text_pos, text_str, text_font_size
):
    text = build_text(
        pos=text_pos,
        text=text_str,
        font=None,  # type: ignore because get_text_width is mocked
        font_size=text_font_size,
        horizontal_align="right",
    )

    assert text.pos == Point(x=100.0, y=100)  # Adjusted for right alignment


@patch("newsflash.svg.elements.text.get_text_width", return_value=100.0)
def test_build_text_align_top(get_text_width_mock, text_pos, text_str, text_font_size):
    text = build_text(
        pos=text_pos,
        text=text_str,
        font=None,  # type: ignore because get_text_width is mocked
        font_size=text_font_size,
        vertical_align="top",
    )

    assert (
        text.pos == Point(x=200.0, y=116.0)  # plus font size
    )  # Adjusted for top alignment


@patch("newsflash.svg.elements.text.get_text_width", return_value=100.0)
def test_build_text_align_middle(
    get_text_width_mock, text_pos, text_str, text_font_size
):
    text = build_text(
        pos=text_pos,
        text=text_str,
        font=None,  # type: ignore because get_text_width is mocked
        font_size=text_font_size,
        vertical_align="middle",
    )

    assert (
        text.pos == Point(x=200.0, y=104.0)  # plus a quarter font size
    )  # Adjusted for top alignment


@patch("newsflash.svg.elements.text.get_text_width", return_value=100.0)
def test_build_text_align_bottom(
    get_text_width_mock, text_pos, text_str, text_font_size
):
    text = build_text(
        pos=text_pos,
        text=text_str,
        font=None,  # type: ignore because get_text_width is mocked
        font_size=text_font_size,
        vertical_align="bottom",
    )

    assert (
        text.pos == Point(x=200.0, y=96.0)  # minus a quarter font size
    )  # Adjusted for top alignment


@fixture
def test_text() -> Text:
    return Text(
        pos=Point(x=100, y=200),
        text="Hello, World!",
        width=150,
        font_size=24,
    )


def test_text_top(test_text: Text):
    assert test_text.top == 176  # 200 - 24


def test_text_right(test_text: Text):
    assert test_text.right == 250  # 100 + 150


def test_text_bottom(test_text: Text):
    assert test_text.bottom == 208  # 200 + 24 / 3


def test_text_left(test_text: Text):
    assert test_text.left == 100


def test_text_height(test_text: Text):
    assert test_text.height == 32  # 24 * 4 / 3


def test_text_render():
    text = Text(
        pos=Point(x=50, y=75),
        text="Sample Text",
        width=120,
        font_size=18,
        classes=["sample-class"],
        styles=["fill: red;"],
        attributes={"data-info": "example", "aria-label": "sample text"},
    )

    result = text.render()
    expected = """<text 
    class="sample-class" 
    x="50.0" 
    y="75.0" 
    style="fill: red;"
    data-info="example"
    aria-label="sample text"
>
    Sample Text
</text>"""
    assert result == expected
