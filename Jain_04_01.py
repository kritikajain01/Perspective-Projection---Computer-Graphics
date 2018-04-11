# Jain, Kritika
# 1002-093-381
# 2017-10-25
# Assignment_04_01

import tkinter as tk
import Jain_04_02 as j02  # This module includes all the widgets
import Jain_04_03 as j03  # This module includes graphic components


def close_window_callback(root):
    if tk.messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()

ob_root_window = tk.Tk()
ob_root_window.protocol("WM_DELETE_WINDOW", lambda root_window=ob_root_window: close_window_callback(root_window))
ob_world = j03.cl_world()
j02.cl_widgets(ob_root_window, ob_world)
ob_root_window.mainloop()
