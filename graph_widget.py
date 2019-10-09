import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

def figure_widget(master, x, y):

    fig = Figure(figsize=(5, 4), dpi=100)
    xx = np.array(x)
    yy = np.array(y)
    fig.add_subplot(111).plot(xx, yy)

    canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
    canvas.draw()

    return canvas.get_tk_widget()
    # returning the widget of the canvas, not the canvas itself, so we can treat it
    # like any other widget and pack it, etc.

