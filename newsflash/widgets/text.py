from pydantic import BaseModel

from .widgets import Widget


class ValueDisplay(Widget):
    template: tuple[str, str] = ("widgets", "value_display.html")
    label: str = ""
    value: str = ""


class Paragraph(Widget):
    template: tuple[str, str] = ("widgets", "paragraph.html")
    text: str = ""


class Notification(BaseModel):
    message: str = ""
    level: str  # could be 'info', 'warning', 'error', etc.
    duration: int  # duration in milliseconds


class Notifications(Widget):
    id: str = "newsflash-notifications-container"
    template: tuple[str, str] = ("widgets", "notifications.html")
    notifications: list[Notification] = []  # List of notifications to display

    def push(self, message: str, level: str = "info", duration: int = 5000) -> None:
        notification = Notification(
            message=message,
            level=level,
            duration=duration,
        )
        self.notifications.append(notification)
