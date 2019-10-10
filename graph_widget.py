import tkinter

import random

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import types

import numpy as np

xx = None
yy = None


class MyGraphWidget(object):

    """This creates a tkinter canvas object but adds references to the underlying matplotlib graph
    and binds a method to update/redraw the canvas."""

    def __new__(cls, master, x, y):

        fig = Figure(figsize=(5, 4), dpi=100)
        fig.add_subplot(111).plot(x, y)
        canvas = FigureCanvasTkAgg(fig, master=master)
        wid = canvas.get_tk_widget()
        wid.canvas = canvas
        wid.fig = fig
        wid.refresh = types.MethodType(MyGraphWidget.refresh, wid)
        # this binds the refresh method to the widget instance
        return wid
        # return the tkinter canvas object rather than a different class, so we can access all
        # its usual methods for setting up the tkinter layout

    def refresh(self, x, y):

        # print(f"x and y ids are {id(x)}, {id(y)}")
        self.fig.clear()
        self.fig.add_subplot(111).plot(x, y)
        self.canvas.draw()


def figure_widget(master, x, y):

    fig = Figure(figsize=(5, 4), dpi=100)
    global xx
    global yy
    xx = x
    yy = y
    fig.add_subplot(111).plot(xx, yy)

    return my_get_widget(fig, master)
    # returning the widget of the canvas, not the canvas itself, so we can treat it
    # like any other widget and pack it, etc.


def my_get_widget(fig, master):

    canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
    canvas.draw()
    wid = canvas.get_tk_widget()
    wid.redraw = lambda: canvas.draw()
    wid.refresh = lambda xx, yy: redraw_fig(fig, xx, yy)
    return wid


def redraw_fig(fig, xx, yy):

    fig.clear()
    fig.add_subplot(111).plot(xx, yy)

