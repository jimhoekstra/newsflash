from typing import Any, Type

from pydantic import create_model

from .widgets import Widget
from .inputs import Button
from .text import Paragraph



class CompositeWidget(Widget):
    components: list[Type[Widget]] = []

    def get_components(self) -> list[Type[Widget]]:
        return self.components


class CardContent(Paragraph):
    _parent: "Card | None" = None


class CardButton(Button):
    _parent: "Card | None" = None

    _callback_fn_name: str = "on_button_click"
    _callback_fn_on_parent: bool = True


class Card(CompositeWidget):
    template: tuple[str, str] = ("widgets", "card.html")
    content: str = ""
    buttons: list[tuple[str, str]] = []

    def model_post_init(self, context) -> None:
        card_content = create_model(
            "CardContent",
            __base__=CardContent,
            text=(str, self.content),
            id=(str, f"{self.id}-content"),
            _parent=(Type["Card"], self),
        )

        buttons: list[Type[Widget]] = []
        for button in self.buttons:
            card_button = create_model(
                "CardButton",
                __base__=CardButton,
                id=(str, f"{self.id}-button-{button[0]}"),
                label=(str, button[1]),
                _parent=(Type["Card"], self),
            )
            buttons.append(card_button)

        self.components = [
            card_content,
        ]
        self.components.extend(buttons)

    def modify_context(self, context: dict[str, Any]) -> dict[str, Any]:
        button_widgets: dict[str, str] = {}

        for widget_id, rendered_widget in context.get("widgets", {}).items():
            if widget_id.startswith(self.id + "-button"):
                button_widgets[widget_id] = rendered_widget

        context["button_widgets"] = button_widgets
        return context

    def on_button_click(self, *args, **kwargs) -> list[Widget]:
        return []
