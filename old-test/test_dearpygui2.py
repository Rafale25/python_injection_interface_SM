#! /usr/bin/python3

import time
import dearpygui.dearpygui as dpg

# value = 0.0

with dpg.value_registry():
	id = dpg.add_float_value(default_value=0.0)
	# dpg.add_int_value(default_value=0, id="float_value")
	# id = dpg.add_string_value(default_value="Default string")


with dpg.window(label="Tutorial", id="main_window"):
	# dpg.add_input_text(label="Text Input 1", source=id)
	dpg.add_input_float(default_value=0, source=id)
	dpg.add_button(label="delete", callback=lambda: dpg.delete_item(id))
	# dpg.add_text(label="0.0", source="")


dpg.setup_viewport()
dpg.set_viewport_title(title="Test")
dpg.set_viewport_width(200)
dpg.set_viewport_height(100)

dpg.set_primary_window("main_window", True)

while dpg.is_dearpygui_running():
	# value += 0.1
	print(dpg.get_value(id))

	dpg.render_dearpygui_frame()
	time.sleep(1 / 40)

dpg.cleanup_dearpygui()

# dpg.start_dearpygui()
