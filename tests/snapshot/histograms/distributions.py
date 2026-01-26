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
            values=[random.gauss(10, 2) for _ in range(9000)],
            num_bins=20,
        )

        return chart._render_update()


class BetaDistributionHistogram(SnapshotTest):
    name: str = "Beta Distribution Histogram"
    path_to_rendered: Path = Path(__file__).parent / "rendered" / "beta.html"
    description: str = """
        Expected to see a histogram representing a Beta distribution with 20 bins.
        The data consists of 1000 samples drawn from a Beta distribution with parameters alpha=2 and beta=5.
        The width of the chart is 600 pixels.
    """

    @staticmethod
    def render() -> str:
        chart = Histogram(
            width=600,
            height=400,
        )

        chart.title = "Beta Distribution Histogram"
        random.seed(42)

        chart.set_values(
            values=[random.betavariate(2, 5) for _ in range(9000)],
            num_bins=20,
        )

        return chart._render_update()


class UniformDistributionHistogram(SnapshotTest):
    name: str = "Uniform Distribution Histogram"
    path_to_rendered: Path = Path(__file__).parent / "rendered" / "uniform.html"
    description: str = """
        Expected to see a histogram representing a Uniform distribution with 20 bins.
        The data consists of 1000 samples drawn from a Uniform distribution between 0 and 1.
        The width of the chart is 600 pixels.
    """

    @staticmethod
    def render() -> str:
        chart = Histogram(
            width=600,
            height=400,
        )

        chart.title = "Uniform Distribution Histogram"
        random.seed(42)

        chart.set_values(
            values=[random.uniform(0, 1) for _ in range(9000)],
            num_bins=20,
        )

        return chart._render_update()
