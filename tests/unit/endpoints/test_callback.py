# # from newsflash.endpoints.callback import _get_callback_inputs
# from newsflash.widgets.widgets import Widget
# from newsflash.endpoints.parsers import RequestValues


# class DummyInputWidget(Widget):
#     pass


# class DummyWidget(Widget):
#     _callback_fn_name: str = "test_callback"

#     def test_callback(self, input_widget: DummyInputWidget) -> list[Widget]: ...


# def test_get_callback_inputs():
#     request_values = RequestValues(
#         url_path="/test",
#         trigger_element_id="test-trigger",
#         widget_attributes={},
#     )

#     widget = DummyWidget(
#         request_values=request_values,
#     )
#     widget._post_init()

#     result = widget._get_callback_inputs()

#     assert "input_widget" in result
