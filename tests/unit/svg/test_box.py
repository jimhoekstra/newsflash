from pytest import fixture, approx

from newsflash.svg.box import Box, scale_x_to_box, scale_y_to_box


@fixture
def default_box() -> Box:
    return Box(
        top=0,
        right=100,
        bottom=100,
        left=0,
        top_y_value=0.0,
        right_x_value=1.0,
        bottom_y_value=1.0,
        left_x_value=0.0,
    )


def test_simple(default_box):
    new_x = scale_x_to_box(0.4, default_box)
    assert new_x == 40

    new_y = scale_y_to_box(0.6, default_box)
    assert new_y == 60


def test_reversed_x(default_box):
    default_box.right_x_value = 0.0
    default_box.left_x_value = 1.0

    new_x = scale_x_to_box(0.4, default_box)
    assert new_x == 60

    new_y = scale_y_to_box(0.6, default_box)
    assert new_y == 60


def test_reversed_y(default_box):
    default_box.top_y_value = 1.0
    default_box.bottom_y_value = 0.0

    new_x = scale_x_to_box(0.4, default_box)
    assert new_x == 40

    new_y = scale_y_to_box(0.6, default_box)
    assert new_y == 40


def test_x_padding_same_left_right(default_box):
    default_box.padding_left = 0.1
    default_box.padding_right = 0.1

    new_x = scale_x_to_box(0.1, default_box)
    # 10 for padding and 10 for scaled value, 100 for width plus 20 for padding
    # times 100 for scale correction
    assert new_x == approx((10 + 10) / (100 + 20) * 100)


def test_x_padding_different_left_right_a(default_box):
    default_box.padding_left = 0.1
    default_box.padding_right = 0.2

    new_x = scale_x_to_box(0.3, default_box)
    # 10 for padding and 30 for scaled value, 100 for width plus 30 for padding
    # times 100 for scale correction
    assert new_x == approx((30 + 10) / (100 + 30) * 100)


def test_y_padding(default_box):
    default_box.padding_top = 0.1
    default_box.padding_bottom = 0.1

    new_y = scale_y_to_box(0.1, default_box)
    # 10 for padding and 10 for scaled value, 100 for width plus 20 for padding
    # times 100 for scale correction
    assert new_y == approx((10 + 10) / (100 + 20) * 100)


def test_y_padding_different_top_bottom_a(default_box):
    default_box.padding_top = 0.1
    default_box.padding_bottom = 0.05

    new_y = scale_y_to_box(0.25, default_box)
    # 10 for padding and 25 for scaled value, 100 for width plus 15 for padding
    # times 100 for scale correction
    assert new_y == approx((25 + 10) / (100 + 15) * 100)
