from newsflash.svg.elements.path import Path, build_path
from newsflash.svg.utils import Point
from newsflash.svg.box import Box


def test_build_path():
    points = [Point(x=0, y=0), Point(x=50, y=100), Point(x=75, y=50), Point(x=100, y=0)]

    path = build_path(points=points)
    expected = Path(
        points=points,
        path_length=100.0,
        classes=[],
        styles=[],
        attributes={},
    )

    assert path == expected


def test_build_path_with_box():
    points = [
        Point(x=0, y=0),
        Point(x=0.5, y=1.0),
        Point(x=0.7, y=0.5),
        Point(x=1.0, y=0.0),
    ]
    box = Box(top=0, right=200, bottom=200, left=0)

    path = build_path(points=points, box=box)
    expected_points = [
        Point(x=0, y=0),
        Point(x=100, y=200),
        Point(x=140, y=100),
        Point(x=200, y=0),
    ]
    expected = Path(
        points=expected_points,
        path_length=100.0,
        classes=[],
        styles=[],
        attributes={},
    )

    assert path == expected
