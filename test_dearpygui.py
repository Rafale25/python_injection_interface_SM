#! /usr/bin/python3

import dearpygui.dearpygui as dpg


# import dearpygui.dearpygui as dpg
# from dearpygui.demo import show_demo
# show_demo()
# dpg.start_dearpygui()
# exit()


VIEWPORT_WIDTH = 600
VIEWPORT_HEIGHT = 400
VIEWPORT_MIN_WIDTH = 600
VIEWPORT_MIN_HEIGHT = 200


with dpg.window(id="main_window", menubar=True):

	# with dpg.child(border=False):
	#
	# 	# with dpg.table(header_row=False, borders_innerV=True):
	# 	#
	# 	# 	dpg.add_table_column()
	# 	# 	dpg.add_table_column()
	# 	# 	dpg.add_table_column()
	# 	#
	# 	# 	dpg.add_text("MDR0")
	# 	# 	dpg.add_table_next_column()
	# 	#
	# 	# 	dpg.add_text("Heyeyyyy0")
	# 	# 	dpg.add_table_next_column()
	# 	#
	# 	# 	dpg.add_text("Salut2")
	# 	# 	dpg.add_table_next_column()

	# with dpg.child(id="INPUT", autosize_x=True, border=True):
	# 	pass
	#
	# dpg.add_same_line()
	#
	# with dpg.child(id="MODULE", autosize_x=True, border=True):
	# 	pass
	#
	# dpg.add_same_line()
	# with dpg.child(id="OUTPUT", autosize_x=True, border=True):
	# 	pass
		with dpg.window(
			label="Input", id="window_input", no_move=True, no_collapse=True, no_close=True,
			min_size=(VIEWPORT_WIDTH/3, VIEWPORT_HEIGHT)):

			dpg.add_text("Hello World")

			with dpg.group():

				dpg.add_button(label="data", id="myButton")
				with dpg.tooltip(parent="myButton"):
					dpg.add_text("LOT OF DATA HERE")
				with dpg.drag_payload(parent="myButton", id="payloadData", drag_data=[42, 69], payload_type="data"):
					dpg.add_text("data")


				# def MyLambda(id, value):
				# 	dpg.set_item_label(id, value[0])
				# 	print(value)

				dpg.add_text("Thrust")
				dpg.add_same_line()
				# dpg.add_button(label="", width=75, height=20, enabled=False, payload_type="data", drop_callback=MyLambda) #user_data=
				dpg.add_button(label="", width=75, height=20, enabled=False, payload_type="data", drop_callback=lambda id, value: dpg.set_item_label(id, value[0])) #user_data=


		with dpg.window(
			label="Module", id="window_module", no_move=True, no_collapse=True, no_close=True,
			min_size=(VIEWPORT_WIDTH/3, VIEWPORT_HEIGHT)):
			pass

		with dpg.window(
			label="Output", id="window_output", no_move=True, no_collapse=True, no_close=True,
			min_size=(VIEWPORT_WIDTH/3, VIEWPORT_HEIGHT)):
			pass

def resize_viewport(_, size):
	viewport_width = dpg.get_viewport_width()
	viewport_height = dpg.get_viewport_height()

	# for i, window in enumerate(("INPUT", "MODULE", "OUTPUT")):
	for i, window in enumerate(("window_input", "window_module", "window_output")):
		dpg.set_item_pos(item=window, pos=((viewport_width/3) * i, 20))
		dpg.set_item_width(item=window, width=viewport_width/3)
		dpg.set_item_height(item=window, height=viewport_height)


dpg.setup_viewport()
dpg.set_viewport_title(title="Sm Injector Interface")
dpg.set_viewport_width(VIEWPORT_WIDTH)
dpg.set_viewport_height(VIEWPORT_HEIGHT)
dpg.set_viewport_min_width(VIEWPORT_MIN_WIDTH)
dpg.set_viewport_min_height(VIEWPORT_MIN_HEIGHT)
dpg.set_viewport_vsync(True)

dpg.set_viewport_resizable(True)
dpg.set_viewport_resize_callback(resize_viewport)

dpg.set_primary_window("main_window", True)

dpg.start_dearpygui()
