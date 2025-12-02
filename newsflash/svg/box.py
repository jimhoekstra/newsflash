from pydantic import BaseModel

from .utils.point import XCoor, YCoor, Point


class Box(BaseModel):
    top: YCoor
    right: XCoor
    bottom: YCoor
    left: XCoor

    padding_top: float = 0.0
    padding_right: float = 0.0
    padding_bottom: float = 0.0
    padding_left: float = 0.0

    top_y_value: float = 0.0
    right_x_value: float = 1.0
    bottom_y_value: float = 1.0
    left_x_value: float = 0.0

    def apply_padding(self) -> "Box":
        return Box(
            top=self.top,
            right=self.right,
            bottom=self.bottom,
            left=self.left,
            padding_top=0.0,
            padding_right=0.0,
            padding_bottom=0.0,
            padding_left=0.0,
            top_y_value=self.top_y_value - self.padding_top,
            right_x_value=self.right_x_value + self.padding_right,
            bottom_y_value=self.bottom_y_value + self.padding_bottom,
            left_x_value=self.left_x_value - self.padding_left,
        )


def scale_width_to_box(width: float, box: Box) -> float:
    box = box.apply_padding()
    box_width = box.right_x_value - box.left_x_value
    return abs((width / box_width) * (box.right - box.left))


def scale_height_to_box(height: float, box: Box) -> float:
    box = box.apply_padding()
    box_height = box.bottom_y_value - box.top_y_value
    return abs((height / box_height) * (box.bottom - box.top))


def scale_x_to_box(x: XCoor, box: Box) -> XCoor:
    box = box.apply_padding()
    normalized_x = (x - (box.left_x_value + box.padding_left)) / (
        box.right_x_value - box.left_x_value
    )
    return box.left + normalized_x * (box.right - box.left)


def scale_y_to_box(y: YCoor, box: Box) -> YCoor:
    box = box.apply_padding()
    normalized_y = (y - box.top_y_value) / (box.bottom_y_value - box.top_y_value)
    return box.top + normalized_y * (box.bottom - box.top)


def scale_point_to_box(point: Point, box: Box) -> Point:
    return Point(
        x=scale_x_to_box(point.x, box),
        y=scale_y_to_box(point.y, box),
    )
