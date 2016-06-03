#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import Tkinter as tk
import ttk

from winmoncon import PhysicalMonitor


def change(evt):
    monitor.brightness = int(scale.get()) 


if __name__ == '__main__':
    monitor = PhysicalMonitor.all[0]
    print("Monitor %s: %s" % (monitor.description, monitor.technology_type))

    root = tk.Tk() 
    root.resizable(width=tk.TRUE, height=tk.FALSE)
    root.minsize(height=0, width=400)

    min, crt, max = monitor.get_brightness()
    scale = ttk.Scale(root, from_=min, to=max, orient=tk.HORIZONTAL, command=change)
    scale.pack(fill=tk.X, expand=1)
    scale.set(crt)

    root.mainloop()
