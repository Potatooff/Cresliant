import os
import sys
import webbrowser
from tkinter.filedialog import asksaveasfilename

import dearpygui.dearpygui as dpg

from src.editor import node_editor
from src.utils import ImageController as dpg_img
from src.utils.nodes import history_manager
from src.utils.paths import resource_path

VERSION = "v0.1.0"

dpg.create_context()
dpg.create_viewport(title="Cresliant", small_icon=resource_path("icon.ico"), large_icon=resource_path("icon.ico"))

dpg_img.set_texture_registry(dpg.add_texture_registry())
with dpg.font_registry():
    dpg.add_font(resource_path("Roboto-Regular.ttf"), 17, tag="font")
    dpg.bind_font("font")

with dpg.texture_registry():
    dpg.add_static_texture(1, 1, [0] * 1 * 1 * 4, tag="output_0")


def export():
    image = dpg.get_item_user_data("Output").image
    location = asksaveasfilename(
        filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")],
        defaultextension=".png",
        initialfile="output.png",
        initialdir=os.curdir,
    )
    image.save(location)
    if sys.platform == "win32":
        webbrowser.open(location)
    else:
        image.show()


with dpg.window(
    tag="popup_window",
    no_move=True,
    no_close=True,
    no_resize=True,
    no_collapse=True,
    show=False,
    label="Add Node",
    width=200,
):
    for module in node_editor.modules[1:-1]:
        dpg.add_button(label=module.name, tag=module.name + "_popup", callback=module.new, indent=3, width=180)

with dpg.window(
    tag="node_popup_window", no_move=True, no_close=True, no_resize=True, no_collapse=True, show=False, label="Settings"
):
    dpg.add_button(label="Delete node", callback=node_editor.delete_nodes)
    dpg.add_button(label="Duplicate node", callback=node_editor.duplicate_nodes)


def handle_shortcuts(_sender, app_data):
    if not dpg.is_key_down(dpg.mvKey_Control):
        return

    match app_data:
        case dpg.mvKey_V:
            node_editor.duplicate_nodes()
        case dpg.mvKey_N:
            node_editor.reset()
        case dpg.mvKey_E:
            export()
        case dpg.mvKey_S:
            node_editor.save()
        case dpg.mvKey_O:
            node_editor.open()
        case dpg.mvKey_Q:
            dpg.stop_dearpygui()
        case dpg.mvKey_Z:
            history_manager.undo()
        case dpg.mvKey_Y:
            history_manager.redo()


def handle_popup(_sender, app_data):
    if app_data == 1 and dpg.is_item_hovered("MainNodeEditor"):
        if len(dpg.get_selected_nodes("MainNodeEditor")) != 0:
            dpg.focus_item("node_popup_window")
            dpg.show_item("node_popup_window")
            dpg.set_item_pos("node_popup_window", dpg.get_mouse_pos(local=False))
            return

        dpg.focus_item("popup_window")
        dpg.show_item("popup_window")
        dpg.set_item_pos("popup_window", dpg.get_mouse_pos(local=False))
    else:
        dpg.hide_item("popup_window")
        dpg.hide_item("node_popup_window")


with dpg.handler_registry():
    dpg.add_mouse_click_handler(button=1, callback=handle_popup)
    dpg.add_mouse_release_handler(button=0, callback=handle_popup)

    dpg.add_key_press_handler(key=dpg.mvKey_Delete, callback=node_editor.delete_nodes)
    dpg.add_key_press_handler(key=dpg.mvKey_Delete, callback=node_editor.delete_links)

    dpg.add_key_release_handler(key=dpg.mvKey_V, callback=handle_shortcuts)
    dpg.add_key_release_handler(key=dpg.mvKey_N, callback=handle_shortcuts)
    dpg.add_key_release_handler(key=dpg.mvKey_E, callback=handle_shortcuts)
    dpg.add_key_release_handler(key=dpg.mvKey_S, callback=handle_shortcuts)
    dpg.add_key_release_handler(key=dpg.mvKey_O, callback=handle_shortcuts)
    dpg.add_key_release_handler(key=dpg.mvKey_Q, callback=handle_shortcuts)
    dpg.add_key_release_handler(key=dpg.mvKey_Z, callback=handle_shortcuts)
    dpg.add_key_release_handler(key=dpg.mvKey_Y, callback=handle_shortcuts)

    # Dev tools
    if node_editor.debug:
        dpg.add_key_release_handler(key=dpg.mvKey_F10, callback=dpg.show_item_registry)
        dpg.add_key_release_handler(key=dpg.mvKey_F11, callback=dpg.show_style_editor)
        dpg.add_key_release_handler(key=dpg.mvKey_F12, callback=dpg.show_metrics)


with dpg.window(
    tag="Cresliant",
    menubar=True,
    no_title_bar=True,
    no_move=True,
    no_resize=True,
    no_collapse=True,
    no_close=True,
):
    with dpg.menu_bar():
        with dpg.menu(tag="file", label="File"):
            dpg.add_menu_item(tag="new", label="New Project", shortcut="Ctrl+N", callback=node_editor.reset)
            dpg.add_menu_item(tag="open", label="Open Project...", shortcut="Ctrl+O", callback=node_editor.open)
            dpg.add_separator()
            dpg.add_menu_item(tag="save", label="Save Project...", shortcut="Ctrl+S", callback=node_editor.save)
            dpg.add_menu_item(tag="export", label="Export Output...     ", shortcut="Ctrl+E", callback=export)
            dpg.add_separator()
            dpg.add_menu_item(tag="close", label="Quit", shortcut="Ctrl+Q", callback=dpg.stop_dearpygui)

        with dpg.menu(tag="edit", label="Edit"):
            dpg.add_menu_item(label="Undo    ", tag="undo", shortcut="Ctrl+Z", callback=history_manager.undo)
            dpg.add_menu_item(label="Redo    ", tag="redo", shortcut="Ctrl+Y", callback=history_manager.redo)

        with dpg.menu(tag="nodes", label="Nodes"):
            for module in node_editor.modules[1:]:
                dpg.add_menu_item(tag=module.name, label=module.name, callback=module.new)

        with dpg.menu(tag="about", label="About"):
            dpg.add_menu_item(
                tag="github",
                label="View it on Github",
                callback=lambda: webbrowser.open("https://github.com/Cresliant/Cresliant"),
            )
            dpg.add_separator()
            dpg.add_menu_item(tag="version", label="Cresliant " + VERSION, enabled=False)

    dpg.add_text("Ctrl+Click to remove a link.", bullet=True)
    node_editor.start()


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.maximize_viewport()
dpg.set_primary_window("Cresliant", True)
dpg.start_dearpygui()
dpg.destroy_context()
