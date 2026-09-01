import abc
import typing

from newsflash.models import Element
from newsflash.templates import template_registry


class BaseElement(Element, abc.ABC):
    """Abstract base class for newsflash Elements."""

    def render(
        self,
        trigger_context_getter: typing.Callable[
            [str, list[str]], dict[str, str | bool]
        ],
        hx_swap_oob: str | None,
    ) -> str:
        """Render an Element to an HTML string.
        
        Parameters
        ----------
        trigger_context_getter
            A function that takes an element ID and a list of triggers, and returns
            the context needed to include the htmx-enabled interactivity in the 
            rendered HTML returned from this method.
        hx_swap_oob
            A flag that adds the `hx-swap-oob="true"` flag to the rendered HTML
            that ensures that htmx replaces an existing element on the page with
            the new render returned from this method if the ID matches.

        Returns
        -------
        The rendered element as an HTML string.
        """
        template = template_registry.get_template(
            dir_name=self.template_dir_name,
            template_file_name=self.template_name,
        )

        trigger_context = trigger_context_getter(self.id, self.all_triggers)

        rendered = template.render(
            {
                **self.model_dump(exclude={"_children"}),
                "hx_swap_oob": hx_swap_oob,
                "elements": {
                    element.id: element.render(
                        trigger_context_getter=trigger_context_getter, hx_swap_oob=None
                    )
                    for element in self.compose()
                },
                **trigger_context,
            }
        )

        return rendered

    def compose(self) -> typing.Iterable["Element"]:
        """Compose the children of the element.
        
        If subclasses of BaseElement don't overwrite this method, then return
        the elements in the children attribute, if any.

        Returns
        -------
        An iterable of Elements.
        """
        yield from self.children
