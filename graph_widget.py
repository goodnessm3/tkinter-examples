from tkinter import *

# import random

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure

import types


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

        self.fig.clear()
        self.fig.add_subplot(111).plot(x, y)
        self.canvas.draw()


class MyOtherGraphWidget(Frame):

    """more straightforward way to have a custom graph widget by embedding the graph and canvas object in
    a frame, then using the parent frame to do the packing, etc, in the UI. This is probably the best way."""

    def __init__(self, *args, xdata=None, ydata=None, **kwargs):

        super().__init__(*args, **kwargs)
        if not(xdata and ydata):
            raise ValueError("must provide x and y data arrays")
        else:
            self.xdata = xdata
            self.ydata = ydata

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(xdata, ydata)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        widget = self.canvas.get_tk_widget()
        widget.pack(side=TOP, fill=BOTH, expand=YES)

    def refresh(self):

        self.fig.clear()
        self.fig.add_subplot(111).plot(self.xdata, self.ydata)
        self.canvas.draw()


class EventGraph(Frame):

    def __init__(self, *args, xdata=None, ydata=None, **kwargs):

        super().__init__(*args, **kwargs)
        if not (xdata and ydata):
            raise ValueError("must provide x and y data arrays")
        else:
            self.xdata = xdata
            self.ydata = ydata

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(xdata, ydata, picker=5)  # the tolerance for picking with mouse cursor
        self.selected = None

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.mpl_connect("pick_event", self.onpick)  # bind an event for clicking on graph
        widget = self.canvas.get_tk_widget()
        widget.pack(side=TOP, fill=BOTH, expand=YES)

    def refresh(self):

        self.fig.clear()
        self.fig.add_subplot(111).plot(self.xdata, self.ydata)
        self.canvas.draw()

    def onpick(self, e):

        if self.selected:
            self.ax.lines.pop()  # remove the last Line2D object that we plotted
        self.selected = self.ax.plot([self.xdata[e.ind[0]]], [self.ydata[e.ind[0]]], "ro")
        # the event has an "index" of the data point, but it's returned as a single value list
        self.canvas.draw()  # need to refresh the canvas
        # print(self.selected)
        # print(dir(self.selected))


def figure_widget(master, x, y):

    """Another way to do a custom graph widget,
    function that returns the tk widget of a graph canvas, after adding some properties and methods
    to store references to the data and refresh the plot."""

    fig = Figure(figsize=(5, 4), dpi=100)
    fig.add_subplot(111).plot(x, y)

    return my_get_widget(fig, master, x, y)
    # returning the widget of the canvas, not the canvas itself, so we can treat it
    # like any other widget and pack it, etc.


def my_get_widget(fig, master, xdata, ydata):

    canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
    canvas.draw()
    wid = canvas.get_tk_widget()
    wid.redraw = lambda: canvas.draw()
    wid.xdata = xdata
    wid.ydata = ydata
    wid.refresh = lambda xx=wid.xdata, yy=wid.ydata: redraw_fig(fig, xx, yy)
    return wid


def redraw_fig(fig, xx, yy):

    fig.clear()
    fig.add_subplot(111).plot(xx, yy)


class MyPieWidget(Frame):

    """custom frame containing a pie chart"""

    def __init__(self, *args, data_series=None, **kwargs):

        """data_series is a pair of lists [name1, name2...], [value1, value2...]
        https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.pie.html"""

        super().__init__(*args, **kwargs)
        self.fig = Figure(figsize=(6, 4), dpi=100)
        names, data = data_series  # unpack the passed arg
        ax = self.fig.add_subplot(111)  # add_subplot returns an axes object
        wedges, text, autopct = ax.pie(data, autopct=lambda x: f"{int(x)}% ", textprops={"color": "w"})
        # the autopct lambda function gets passed the percentage as an argument
        ax.legend(wedges, names, title="title", loc="center left",
                  bbox_to_anchor=(1, 1))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        widget = self.canvas.get_tk_widget()
        widget.pack(side=TOP, fill=BOTH, expand=YES)
        self.canvas.mpl_connect('figure_enter_event', lambda x: print(dir(x)))
