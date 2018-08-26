#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import Tkinter as tk
import ttk
import json
import time
import winmoncon as wm

from datetime import datetime
from threading import Thread
from collections import namedtuple
from os.path import expanduser


HourVal = namedtuple('HourVal', ['h', 'v'])


def loop24h(hour_values):
    a, z = hour_values[0], hour_values[-1]
    return [HourVal(z.h - 24, z.v)] + hour_values + [HourVal(a.h + 24, a.v)]


class Canvas(tk.Canvas):

    def __init__(self, root, hour_values=[], on_update_points=None):
        tk.Canvas.__init__(self, root)
        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self.on_add_point)
        self.bind("<Button-3>", self.on_remove_point)
        self.poly, self.vert = None, None

        self.hour_values = [
            HourVal(h, v) for h, v in hour_values
        ]
        self.points = []
        self.handles = []
        self.on_update_points = on_update_points

    def update_points(self):
        if not self.hour_values:
            self.points = [(-5, self.h / 2), (self.w + 5, self.h / 2)]
        else:
            self.points = [
                self.get_xy(hv.h, hv.v) for hv in loop24h(self.hour_values)
            ]

        for h in self.handles:
            self.delete(h)
        self.handles = [
            self.create_oval(
                (x - 5, y - 5, x + 5, y + 5), outline='#1aa', width=2
            )
            for x, y in self.points
        ]

        if not self.poly:
            self.poly = self.create_line(
                *self.points, fill='#555', smooth='', width=2
            )
        else:
            flat_coords = [x for coords in self.points for x in coords]
            self.coords(self.poly, *flat_coords)

        if self.on_update_points:
            self.on_update_points()

    def get_hour_value(self, x, y):
        return HourVal(h=24.0 * x / self.w, v=100 * (self.h - y) / self.h)

    def get_xy(self, hour, value):
        return (self.w * hour / 24.0, self.h * (100.0 - value) / 100)

    def on_resize(self, evt):
        self.w, self.h = self.winfo_width(), self.winfo_height()
        self.update_points()

    def on_add_point(self, evt):
        self.hour_values.append(self.get_hour_value(evt.x, evt.y))
        self.hour_values.sort(key=lambda x: x.h)
        self.update_points()

    def on_remove_point(self, evt):
        hv = self.get_hour_value(evt.x, evt.y)
        self.hour_values = [
            x for x in self.hour_values
            if abs(x.h - hv.h) > 0.5 or abs(x.v - hv.v) > 5
        ]
        self.update_points()

    def update_hour(self, hour_of_day):
        x = int(self.get_xy(hour_of_day, 0)[0])

        if not self.vert:
            self.vert = self.create_line(x, 0, x, self.h, fill='#f11')
        else:
            self.coords(self.vert, x, 0, x, self.h)

        # Couldn't find a better way to get the y-coordinate for a given x
        for y in range(0, self.h):
            if self.poly in self.find_overlapping(x, y, x + 1, y + 1):
                _, brightness = self.get_hour_value(x, y)
                return brightness


def save_hours():
    with open(expanduser('~/.brux'), 'w') as f:
        hour_values = json.dump(c.hour_values, f)


def load_hours():
    try:
        with open(expanduser('~/.brux')) as f:
            return json.load(f)
    except:
        return []


def tick():
    while True:
        time.sleep(1)
        try:
            d = datetime.now()
            hour_of_day = d.hour + d.minute / 60.0 + d.second / 3600.0
            new_brightness = c.update_hour(hour_of_day)
            _, old_brightness, _ = monitor.get_brightness()
            if new_brightness != old_brightness:
                monitor.brightness = new_brightness
        except:
            pass


if __name__ == '__main__':
    monitor = wm.PhysicalMonitor.all[0]

    root = tk.Tk()
    root.resizable(width=tk.FALSE, height=tk.FALSE)
    root.minsize(height=200, width=600)

    c = Canvas(root, load_hours(), on_update_points=save_hours)
    c.pack(fill=tk.BOTH, expand=1)

    t = Thread(target=tick)
    t.daemon = True
    t.start()

    root.mainloop()