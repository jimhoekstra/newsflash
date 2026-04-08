from typing import Annotated

from pydantic import BaseModel

from newsflash.svg.element import TemplateParam
from .widgets import Widget


class ValueDisplay(Widget):
    template: tuple[str, str] = ("widgets", "value_display.html")
    label: Annotated[str, TemplateParam()] = ""
    value: Annotated[str, TemplateParam()] = ""


class Paragraph(Widget):
    template: tuple[str, str] = ("widgets", "paragraph.html")
    text: Annotated[str, TemplateParam()] = ""


class Notification(BaseModel):
    message: str = ""
    level: str
    duration: int  # duration in milliseconds


class Notifications(Widget):
    id: Annotated[str, TemplateParam()] = "newsflash-notifications-container"
    template: tuple[str, str] = ("widgets", "notifications.html")
    notifications: Annotated[
        list[Notification], TemplateParam()
    ] = []  # List of notifications to display

    def push(self, message: str, level: str = "info", duration: int = 5000) -> None:
        notification = Notification(
            message=message,
            level=level,
            duration=duration,
        )
        self.notifications.append(notification)
