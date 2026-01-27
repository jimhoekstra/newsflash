from pathlib import Path

from newsflash.widgets import BarChart
from ..snapshot_test import SnapshotTest


class DescendingBarChart5(SnapshotTest):
    name: str = "Descending Bar Chart 5"
    path_to_rendered: Path = Path(__file__).parent / "rendered" / "descending-5.html"
    description: str = """
        Expected to see five bars labelled A to E with heights decreasing from 
        left to right in steps of 30. The width of the chart is 600 pixels.
    """

    @staticmethod
    def render() -> str:
        chart = BarChart(
            width=600,
            height=400,
        )

        chart.title = "Ascending Bar Chart"

        chart.set_values(
            values=[150, 120, 90, 60, 30],
            labels=["A", "B", "C", "D", "E"],
        )

        return chart._render_update()


class DescendingBarChartLargeNumbers(SnapshotTest):
    name: str = "Descending Bar Chart Large Numbers"
    path_to_rendered: Path = (
        Path(__file__).parent / "rendered" / "descending-large-numbers.html"
    )
    description: str = """
        Expected to see five bars labelled A to E with heights decreasing from 
        left to right in steps of 1,000,000. The left starting point is 10,000,000.
        The width of the chart is 600 pixels.
        The y-axis is expected to scale appropriately to accommodate the large numbers,
        and display a multiplier of x1,000.000 above the y-axis.
    """

    @staticmethod
    def render() -> str:
        chart = BarChart(
            width=600,
            height=400,
        )

        chart.title = "Large Numbers"

        chart.set_values(
            values=[10_000_000, 9_000_000, 8_000_000, 7_000_000, 6_000_000],
            labels=["A", "B", "C", "D", "E"],
        )

        return chart._render_update()
