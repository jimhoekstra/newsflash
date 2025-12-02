from pydantic import BaseModel


type XCoor = float
type YCoor = float


class Point(BaseModel):
    x: XCoor
    y: YCoor
