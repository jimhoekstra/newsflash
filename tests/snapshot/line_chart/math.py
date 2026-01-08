from pathlib import Path
from math import sin, pi

from newsflash.widgets import LineChart
from ..snapshot_test import SnapshotTest


class SineLine(SnapshotTest):
    name: str = "Sine Line"
    path_to_rendered: Path = Path(__file__).parent / "rendered" / "sine-line.html"
    description: str = """
        Expected to see a line chart plotting a sine wave from 0 to 2 pi. The width 
        of the chart is 600 pixels.
    """

    @staticmethod
    def render() -> str:
        chart = LineChart(
            width=600,
            height=400,
        )

        chart.title = "Ascending Line Chart"

        xs = [x / 100 * 2 * pi for x in range(100)]
        ys = [sin(x) for x in xs] 

        chart.set_values(xs=xs, ys=ys)

        return chart._render_update()