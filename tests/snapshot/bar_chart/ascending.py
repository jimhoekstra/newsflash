from pathlib import Path

from newsflash.widgets import BarChart
from ..snapshot_test import SnapshotTest


class AscendingBarChart5(SnapshotTest):
    name: str = "Ascending Bar Chart 5"
    path_to_rendered: Path = Path(__file__).parent / "rendered" / "ascending-5.html"
    description: str = """
        Expected to see five bars labelled A to E with heights increasing from 
        left to right in steps of 10. The width of the chart is 600 pixels.
    """

    @staticmethod
    def render() -> str:
        chart = BarChart(
            width=600,
            height=400,
        )

        chart.title = "Ascending Bar Chart"

        chart.set_values(
            values=[10, 20, 30, 40, 50],
            labels=["A", "B", "C", "D", "E"],
            step=10,
        )

        return chart._render_update()


class AscendingBarChart20(SnapshotTest):
    name: str = "Ascending Bar Chart 20"
    path_to_rendered: Path = Path(__file__).parent / "rendered" / "ascending-20.html"
    description: str = """
        Expected to see twenty bars labelled 1 to 20 with heights increasing from 
        left to right in steps of 5. The width of the chart is 600 pixels.
    """

    @staticmethod
    def render() -> str:
        chart = BarChart(
            width=600,
            height=400,
        )

        chart.title = "Ascending Bar Chart"

        chart.set_values(
            values=[x * 5 for x in range(1, 21)],
            labels=[str(x) for x in range(1, 21)],
            step=20,
        )

        return chart._render_update()
