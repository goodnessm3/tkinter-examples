from tkinter import *
import random


def random_colour():

    """tkinter can understand RGB values like #RRGGBB where the values are hex digits"""

    vals = [hex(x) for x in [random.randint(0, 255) for _ in range(3)]]
    out = "".join([x[2:].zfill(2) for x in vals])
    return f"#{out}"


def register_function(f):

    """Decorator to mark functions as able to appear in context menus for binding to widgets"""

    f.my_function = True
    return f


class DeBugMixIn:

    """middle click -> print the object's dictionary"""

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.bind("<Button-2>", self.dump)

    def dump(self, e):

        print(dir(self))


class RightClickAssignMixIn:

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.bind("<Button-3>", self.right_click_menu)
        self.bound = False  # the func id of a bound method
        self.clear_function()

    def right_click_menu(self, e):

        men = Menu(tearoff=0)
        for k, v in globals().items():
            try:
                if v.my_function:
                    men.add_command(label=f"Bind {v.__name__}",
                                    command=lambda x=v: self.bind_function(x))
            except AttributeError:
                pass

        if self.bound:
            # provide a way to unbind assigned functions if there is one
            men.add_command(label="Unbind function", command=self.clear_function)

        men.tk_popup(e.x_root, e.y_root+40, 0)

    def bind_function(self, func):

        self.configure(command=lambda x=self: func(x))
        self.bound = True  # to remember, if we need to unbind it later

    def clear_function(self):

        self.configure(command=self.dummy_function)
        self.bound = False
        # store the tcl string of the function for comparison purposes later, so we can see
        # if something else was bound in its stead

    def dummy_function(self):

        return


class MyCheckbutton(DeBugMixIn, Checkbutton):

    placeable = True

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


class MyRadiobutton(DeBugMixIn, Radiobutton):

    placeable = True

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


class Mybutton(DeBugMixIn, RightClickAssignMixIn, Button):

    """note the inherited classes have to be in this order for multiple inheritance to work properly."""

    placeable = True

    def __init__(self, *args, **kwargs):

        super().__init__(*args, text=f"Button {id(self)}", **kwargs)


@register_function
def change_colour(caller):

    caller.config(bg=random_colour())


@register_function
def grow(caller):

    old = caller["width"]
    oldh = caller["height"]
    caller.config(width=old+1, height=oldh+1)


def place_widget(e, to_place):

    wid = to_place(master=e.widget)
    wid.place(x=e.x, y=e.y)


def on_right(e):

    men = Menu(tearoff=0)
    for k, v in globals().items():
        try:
            if v.placeable:
                men.add_command(label=f"Place {k} here", command=lambda e=e, v=v: place_widget(e, v))
        except AttributeError:
            pass
    men.tk_popup(e.x_root+10, e.y_root+30, 0)


root = Tk()
f1 = Frame(root, height=500, width=500, relief=SUNKEN)
f1.pack(fill=BOTH, expand=YES)
f1.bind("<Button-3>", on_right)

root.mainloop()
