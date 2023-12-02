from dearpygui import dearpygui as dpg


class OutputModule:
    def __init__(self, texture) -> None:
        self.texture = texture

    name = "Output"
    tooltip = "Image output"

    def run(self):
        if dpg.does_item_exist("Output"):
            dpg.delete_item("Output")

        with dpg.node(
            parent="MainNodeEditor",
            tag="Output",
            label="Output",
            pos=[500, 10],
            user_data=self,
        ):
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data="output"):
                dpg.add_image(self.texture)