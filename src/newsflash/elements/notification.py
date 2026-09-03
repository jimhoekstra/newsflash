from .base import BaseElement


class Notification(BaseElement):
    name: str = "notification"
    # The id is not used in this template so it's fine to leave it empty.
    id: str = ""
    template_dir_name: str = "newsflash-elements"
    template_name: str = "notification.html"
    message: str
