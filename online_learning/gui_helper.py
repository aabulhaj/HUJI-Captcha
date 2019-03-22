import os
import threading
import tkinter as tk

from online_learning.learning_gui import LearningGUI

__DISPLAY__ = None
__ROOT__ = None


def _get_root():
    global __ROOT__
    if __ROOT__ is None:
        root = tk.Tk()
        root.title("Learning GUI")
        __ROOT__ = root
    return __ROOT__


def _get_display_obj():
    global __DISPLAY__
    if __DISPLAY__ is None:
        root = _get_root()
        __DISPLAY__ = LearningGUI(root)
    return __DISPLAY__


class TKthread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    @staticmethod
    def callback():
        os._exit(0)

    def run(self):
        _get_display_obj()
        root = _get_root()
        root.protocol("WM_DELETE_WINDOW", self.callback)
        root.mainloop()


def start_gui():
    TKthread()

    while not __ROOT__ or not __DISPLAY__:
        pass


def close_gui():
    display_obj = _get_display_obj()
    display_obj.add_task(lambda: display_obj.destroy())


def get_input():
    return _get_display_obj().get_input()


def update_gui(image, msg, title):
    display = _get_display_obj()
    display.update_gui(image, msg, title)
