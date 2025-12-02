from newsflash.svg.utils import Point
from newsflash.svg.box import Box
from newsflash.svg.elements import build_line


def test_build_line():
    line = build_line(
        from_pos=Point(x=10, y=20),
        to_pos=Point(x=200, y=100),
        stroke_color="red",
        stroke_width=2.0,
        stroke_linecap="square",
        path_length=5.0,
    )

    assert line.from_pos.x == 10
    assert line.from_pos.y == 20
    assert line.to_pos.x == 200
    assert line.to_pos.y == 100
    assert line.stroke_color == "red"
    assert line.stroke_width == 2.0
    assert line.stroke_linecap == "square"
    assert line.path_length == 5.0


def test_build_line_with_box():
    box = Box(
        top=0,
        right=300,
        bottom=300,
        left=0,
    )

    line = build_line(
        from_pos=Point(x=0.1, y=0.2),
        to_pos=Point(x=0.8, y=0.5),
        stroke_color="blue",
        stroke_width=3.0,
        box=box,
    )

    assert line.from_pos.x == 30  # 0.1 scaled to box width 300
    assert line.from_pos.y == 60  # 0.2 scaled to box height 300
    assert line.to_pos.x == 240  # 0.8 scaled to box width 300
    assert line.to_pos.y == 150  # 0.5 scaled to box height 300
    assert line.stroke_color == "blue"
    assert line.stroke_width == 3.0
    assert line.stroke_linecap == "round"  # default value
    assert line.path_length == 1.0  # default value
