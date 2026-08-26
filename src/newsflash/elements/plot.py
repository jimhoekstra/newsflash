import io

import matplotlib

matplotlib.use("svg")
matplotlib.rcParams["svg.fonttype"] = "none"

from matplotlib.figure import Figure
from matplotlib.axes import Axes
import matplotlib.pyplot as plt

from .base import Element, Trigger


class Plot(Element):
    name: str = "plot"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "plot.html"
    rendered_plot: str = ""
    height: int = 400
    width: int | None = None

    _all_triggers: list[str] = ["revealed"]

    def create_figure(self) -> tuple[Figure, Axes]:
        if self.width is None:
            raise ValueError("can only create figure if width is defined")

        dpi = 100

        fig, ax = plt.subplots(
            figsize=(self.width / dpi, self.height / dpi), dpi=dpi, layout="constrained"
        )

        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)

        return fig, ax

    def set_figure(self, figure: Figure) -> None:
        buf = io.StringIO()
        figure.savefig(buf, format="svg", transparent=True)
        self.rendered_plot = buf.getvalue()

    def revealed(self) -> Trigger:
        return Trigger(
            element_id=self.id,
            element_name=self.name,
            trigger="revealed",
        )
