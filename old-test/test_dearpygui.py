#! /usr/bin/python3

import dearpygui.dearpygui as dpg

with dpg.window(id="main_window"):
	dpg.add_input_float(default_value=0.0, width=125, min_clamped=False, max_clamped=False)

dpg.set_primary_window("main_window", True)

dpg.start_dearpygui()
