#! /usr/bin/python3

import time

import pygame

from injectionAPI import InjectionAPI

from module import Module
from module import ModuleController

from input import Input
from input import InputController

from output import Output
from output import OutputController

from UI import InjectionUI

class InjectionApp:
    def __init__(self):
        self.input_controller = InputController()
        self.module_controller = ModuleController()
        self.output_controller = OutputController()

        pygame.init() # needed because of "pygame.event.get() and pygame.quit()"
        pygame.joystick.init()

        self.injectionAPI = InjectionAPI()
        self.injectionUI = InjectionUI()

    def initialize(self):
        self.injectionAPI.start()
        self.input_controller.scan_joysticks()
        self.input_controller.init_inputs()

        self.module_controller.create_modules_dynamically()

        self.injectionUI.initialize(
            self.injectionAPI, self.input_controller, self.module_controller, self.output_controller)

    def run(self):
        while self.injectionUI.is_running():
            self.injectionUI.update()

            pygame.event.get() #used or it will freeze the program on windows

            self.input_controller.update(self.injectionAPI)
            self.module_controller.compute()

            # print()
            # print(self.module_controller.module_instances[0]._inputs) #DEBUG
            # print("\n".join(str(x) for x in self.output_controller.outputs))
            # print()

            self.output_controller.send_outputs(self.injectionAPI)

            time.sleep(1.0 / 40)

        self.injectionUI.cleanup()
        pygame.quit()

def main():
    app = InjectionApp()
    app.initialize()
    app.run()

if __name__ == '__main__':
    main()

"""
TODO:
- BUG where input can send to wrong module_input ??
"""
