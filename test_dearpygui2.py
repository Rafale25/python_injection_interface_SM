#! /usr/bin/python3

import dearpygui.dearpygui as dpg

# with dpg.group(horizontal=True):

with dpg.window(label="Tutorial"):

	dpg.add_text("value", id="OAO")

	dpg.add_button(label="button", width=75, height=20, callback=lambda: dpg.set_value("OAO", "SALUT"))
	dpg.add_button(label="button", width=75, height=20, callback=lambda: print("HEY"))
	# dpg.add_visible_handler(parent=dpg.last_item(), callback=lambda id: dpg.set_item_label(dpg.last_item(), "42.0"))


	# dpg.add_button(label="", width=75, height=20, enabled=False, payload_type="data")
	# with dpg.drag_payload(parent=dpg.last_item(), drag_data=["yolo", "salut"], payload_type="data"):
	# 	dpg.add_text("input 1")
	#
	# def callback(id, inp, user_data):
	# 	print(f"id is: {id}")
	# 	print(f"inp is: {inp}")
	# 	print(f"user_data is: {user_data}")
	#
	# dpg.add_text("input 1")
	# dpg.add_button(label="", width=75, height=20, enabled=False, payload_type="data", drop_callback=callback, user_data="HEYY")
	# dpg.add_button(label="", width=75, height=20, enabled=False, payload_type="data", drop_callback=lambda id, data: callback(id, data, "heyy"))


dpg.start_dearpygui()
