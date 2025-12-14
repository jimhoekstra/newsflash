from jinja2 import Template
from pydantic import BaseModel

from .templates import widget_templates
from .widgets import Widget


class ValueDisplay(Widget):
    template: Template = widget_templates.get_template("value_display.html")
    label: str = ""
    value: str = ""


class Notification(BaseModel):
    message: str = ""
    level: str  # could be 'info', 'warning', 'error', etc.
    duration: int  # duration in milliseconds


class Notifications(Widget):
    id: str = "newsflash-notifications-container"
    template: Template = widget_templates.get_template("notifications.html")
    notifications: list[Notification] = []  # List of notifications to display

    def push(self, message: str, level: str = "info", duration: int = 5000) -> None:
        notification = Notification(
            message=message,
            level=level,
            duration=duration,
        )
        self.notifications.append(notification)
