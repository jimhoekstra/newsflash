from pathlib import Path
import random

from newsflash.widgets import Histogram
from ..snapshot_test import SnapshotTest


class GaussianDistributionHistogram(SnapshotTest):
    name: str = "Gaussian Distribution Histogram"
    path_to_rendered: Path = Path(__file__).parent / "rendered" / "gauss.html"
    description: str = """
        Expected to see a histogram representing a Gaussian distribution with 20 bins.
        The data consists of 1000 samples drawn from a normal distribution with mean 10 and standard deviation 2.
        The width of the chart is 600 pixels.
    """

    @staticmethod
    def render() -> str:
        chart = Histogram(
            width=600,
            height=400,
        )

        chart.title = "Gaussian Distribution Histogram"
        random.seed(42)

        chart.set_values(
            values=[random.gauss(10, 2) for _ in range(1000)],
            num_bins=20,
        )

        return chart._render_update()