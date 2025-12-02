from pathlib import Path

from pytest import fixture
from fontTools.ttLib import TTFont

from newsflash.svg.utils.fonts import (
    get_text_width,
    get_text_height,
    font_size_to_height,
)


@fixture
def font() -> TTFont:
    path_to_font = (
        Path(__file__).parent.parent.parent.parent.parent
        / "newsflash"
        / "assets"
        / "fonts"
        / "lora"
        / "Lora-Regular.ttf"
    )
    return TTFont(path_to_font)


def test_get_text_width(font: TTFont):
    text = "Hello, World!"
    font_size = 12

    width = get_text_width(font, text, font_size)
    assert isinstance(width, float)
    assert width > 0


def test_get_text_height(font: TTFont):
    text = "Hello, World!"
    font_size = 12

    y_min, y_max = get_text_height(font, text, font_size)
    assert isinstance(y_min, float)
    assert isinstance(y_max, float)
    assert y_min < y_max


def test_font_size_to_height():
    assert font_size_to_height(15) == 20
    assert font_size_to_height(24) == 32
