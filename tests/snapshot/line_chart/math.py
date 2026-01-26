from pathlib import Path
from math import sin, pi, cos

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

        chart.title = "Sine Line Chart"

        xs = [x / 100 * 2 * pi for x in range(101)]
        ys = [sin(x) for x in xs]

        chart.set_values(xs=xs, ys=ys)

        return chart._render_update()


class CosineLine(SnapshotTest):
    name: str = "Cosine Line"
    path_to_rendered: Path = Path(__file__).parent / "rendered" / "cosine-line.html"
    description: str = """
        Expected to see a line chart plotting a cosine wave for 10 periods. The amplitude
        of the wave is 10. The width of the chart is 600 pixels.
    """

    @staticmethod
    def render() -> str:
        chart = LineChart(
            width=600,
            height=400,
        )

        chart.title = "Cosine Line Chart"

        xs = [x / 500 * 20 * pi for x in range(501)]
        ys = [10 * cos(x) for x in xs]

        chart.set_values(xs=xs, ys=ys)

        return chart._render_update()


class SineLineWithCustomLabels(SnapshotTest):
    name: str = "Sine Line Custom Labels"
    path_to_rendered: Path = (
        Path(__file__).parent / "rendered" / "sine-line-with-custom-labels.html"
    )
    description: str = """
        Expected to see a line chart plotting a sine wave for 10 periods. The amplitude
        of the wave is 10. The chart has x labels at every interval of 2*pi. 
        The width of the chart is 600 pixels.
    """

    @staticmethod
    def render() -> str:
        chart = LineChart(
            width=600,
            height=400,
        )

        chart.title = "Sine Line With Custom Labels"

        xs = [x / 500 * 20 * pi for x in range(501)]
        ys = [10 * sin(x) for x in xs]
        x_labels: dict[float, str] = {
            0: "0",
            2 * pi: "2π",
            4 * pi: "4π",
            6 * pi: "6π",
            8 * pi: "8π",
            10 * pi: "10π",
            12 * pi: "12π",
            14 * pi: "14π",
            16 * pi: "16π",
            18 * pi: "18π",
            20 * pi: "20π",
        }

        chart.set_values(xs=xs, ys=ys, x_labels=x_labels)

        return chart._render_update()


class SineLineWithCustomXRange(SnapshotTest):
    name: str = "Sine Line Custom X Range"
    path_to_rendered: Path = (
        Path(__file__).parent / "rendered" / "sine-line-custom-x-range.html"
    )
    description: str = """
        Expected to see a line chart plotting a sine wave for 1 period. The amplitude
        of the wave is 1. The x-axis range is from -2π to 4π. x-labels are set at 0 and 2π.
        The width of the chart is 600 pixels.
    """

    @staticmethod
    def render() -> str:
        chart = LineChart(
            width=600,
            height=400,
        )

        chart.title = "Sine Line With Custom X Range"

        xs = [x / 100 * 2 * pi for x in range(101)]
        ys = [sin(x) for x in xs]
        x_labels: dict[float, str] = {
            0: "0",
            2 * pi: "2π",
        }

        chart.set_values(
            xs=xs, ys=ys, min_x_value=-2 * pi, max_x_value=4 * pi, x_labels=x_labels
        )

        return chart._render_update()
