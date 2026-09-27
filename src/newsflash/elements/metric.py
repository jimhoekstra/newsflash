from .base import BaseElement


class Metric(BaseElement):
    name: str = "metric"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "metric.html"

    label: str
    value: float | int | str
