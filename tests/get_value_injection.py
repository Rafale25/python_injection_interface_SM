import struct
import time
import socket
import subprocess
import atexit

import dearpygui.dearpygui as dpg

class InjectionAPI:
    injector_filepath = "C:/Program Files (x86)/Steam/steamapps/workshop/content/387990/1771470800/sminject.exe"

    def __init__(self):
        self.subprocess = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.address = ('127.0.0.1', 25752)

        self.socket.settimeout(0.1) #1 second timeout

    def start(self):
        try:
            self.subprocess = subprocess.Popen(InjectionAPI.injector_filepath)

            time.sleep(0.5)
            if self.subprocess.poll() != None: #subprocess return None if alive
                print("Error polling subprocess.")
                return -1

            self.scan()
            self.poll()

            atexit.register(self.cleanup)

        except OSError as err:
            print(err)

    def cleanup(self):

        if self.subprocess and self.subprocess.poll() == None:
            self.subprocess.kill()

    def scan(self):
        self.socket.sendto(struct.pack(">B", 0x03), self.address)

    def poll(self):
        self.socket.sendto(struct.pack(">B", 0x04), self.address)

    def set_value(self, id, value):
        packet = bytearray(b'\x01')
        packet.extend(struct.pack(">Id", id, value))
        self.socket.sendto(packet, self.address)

    def _ask_value(self, ids):
        packet = bytearray(b'\x02')
        for id in ids:
            packet.extend(struct.pack(">I", id))

        print("ask_value packet: ", packet) #DEBUG
        self.socket.sendto(packet, self.address)

    def _recv_value(self):
        data = self.socket.recv(1024)
        print("packet data: {}".format(data))

        # -1 for 0x0A byte and divide by 12 because size of channel (4byte) + value(8bytes)
        length = struct.unpack(">h", data[0:2])
        length = (length[0] - 1) // 12

        unpacked_data = struct.unpack(">" + "Id"*length, data[3:])
        # unpacked_data = struct.unpack(">hBId", data)

        print("length: ", length)
        print(unpacked_data)

    def get_value(self, id):
        self.ask_value(id)
        self.recv_value()

app = InjectionAPI()

dpg.setup_viewport()
dpg.set_viewport_title(title="Test get value")
dpg.set_viewport_width(200)
dpg.set_viewport_height(100)
dpg.set_viewport_vsync(True)
dpg.set_viewport_resizable(True)

with dpg.window(id="main_window"):
    dpg.add_button(label="scan", callback=app.scan)
    dpg.add_button(label="poll", callback=app.poll)
    dpg.add_button(label="ask value", callback=lambda: app._ask_value( [0, 1, 2] ))
    dpg.add_button(label="recv value", callback=lambda: app._recv_value())

dpg.set_primary_window("main_window", True)

app.start()

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

    time.sleep(1 / 60)

dpg.cleanup_dearpygui()
