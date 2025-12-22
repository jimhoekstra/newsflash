from pydantic import BaseModel

from .widgets import Widget


class ValueDisplay(Widget):
    template: tuple[str, str] = ("widgets", "value_display.html")
    label: str = ""
    value: str = ""

    include_in_context: set[str] = {"id", "value", "hx_include", "hx_swap_oob", "label", "value"}

    _values_from_request: list[str] = ["label", "value"]


class Paragraph(Widget):
    template: tuple[str, str] = ("widgets", "paragraph.html")
    text: str = ""

    include_in_context: set[str] = {"id", "value", "hx_include", "hx_swap_oob", "text"}

    _values_from_request: list[str] = ["text"]


class Notification(BaseModel):
    message: str = ""
    level: str  # could be 'info', 'warning', 'error', etc.
    duration: int  # duration in milliseconds


class Notifications(Widget):
    id: str = "newsflash-notifications-container"
    template: tuple[str, str] = ("widgets", "notifications.html")
    notifications: list[Notification] = []  # List of notifications to display

    include_in_context: set[str] = {
        "notifications",
    }

    def push(self, message: str, level: str = "info", duration: int = 5000) -> None:
        notification = Notification(
            message=message,
            level=level,
            duration=duration,
        )
        self.notifications.append(notification)
