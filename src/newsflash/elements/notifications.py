from .base import BaseElement


class NotificationContainer(BaseElement):
    name: str = "notification-container"
    id: str = "newsflash-notifications"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "notification-container.html"
