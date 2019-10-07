from tkinter import *
import random
COLOURS = ["ORANGE", "YELLOW", "GREEN", "BLUE", "CYAN", "MAGENTA"]


def RANDOM_COLOUR():

    vals = [hex(x) for x in [random.randint(0, 255) for _ in range(3)]]
    out = "".join([x[2:].zfill(2) for x in vals])
    return f"#{out}"


class MyRoot(Tk):

    """custom root class with extra functions for the rest of the program to use"""

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logging_console = None
        # this is overwritten when a logging console registers itself with the root object

    def log_message(self, message):

        if self.logging_console:
            self.logging_console.log_message(message)


class LoggingMixIn:

    """provides a method to pass string messages that will then be printed to a logging console registered
    with the custom root"""

    _root = None
    # specified so pycharm doesn't complain about unresolved reference, the mixed-in-to class
    # will have this method available

    def log_message(self, message):

        self._root().log_message(message)


class RedSubFrame(Frame):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.config(bg="RED")


class ButtonFrame(Frame, LoggingMixIn):

    def __init__(self, *args, parent_ref=None, **kwargs):

        bg = random.choice(COLOURS)
        super().__init__(*args, background=bg, **kwargs)
        self.parent_ref = parent_ref

        for x in range(0, 5):
            b = Button(self, text=f"Button {x}")
            b.config(command=self.create_button)
            # passing button b as a default argument to the lambda function
            b.pack(expand=YES, fill=BOTH, pady=20)

        lab = Label(self, text="event detector label")
        lab.pack()
        self.bind("<<foo>>", lambda x: print("foo"))

    def button_func(self, calling_button):

        old_colour = calling_button["bg"]  # fetch the background colour from the button's dictionary
        self.log_message(f"Button {id(calling_button)} was clicked.")
        calling_button.config(bg=random.choice(COLOURS))
        calling_button.event_generate("<<foo>>")
        self.after(200, lambda: calling_button.config(bg=old_colour))
        # this will block if it's not a lambda function

    def create_button(self):

        b = Button(self, text=f"Button {random.randint(0,100)}")
        b.config(command=lambda q=b: self.button_func(q))
        b.pack(expand=YES, fill=BOTH)
        b.bind("<Button-3>", self.button_rightclick)

    def button_rightclick(self, e):

        popup = Menu(tearoff=0)
        popup.add_command(label="Delete", command=lambda x=e: self.delete_button_func(e))
        popup.tk_popup(e.x_root, e.y_root, 0)

    def delete_button_func(self, e):

        e.widget.destroy()
        self.log_message(f"Button {id(e.widget)} was destroyed.")


class LoggingConsole(Text):

    """receives messages from the application root object and displays them."""

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.register_with_root()
        self.bind("<Button-3>", self.on_rightclick)
        # we will always be able to get the root reference

    def on_rightclick(self, e):

        popup = Menu(tearoff=0)
        popup.add_command(label="Randomise colour", command=lambda: self.config(bg=RANDOM_COLOUR()))
        popup.tk_popup(e.x_root, e.y_root, 0)

    def log_message(self, message):

        self.insert(END, f"{message}\n")

    def register_with_root(self):

        """place a reference in the root object so it can send messages to this console"""

        self._root().logging_console = self


root = MyRoot()
f1 = Frame(root)
f1.pack(fill=BOTH, expand=YES)
lab = Label(f1, text="test label")
lab.pack()
sub = ButtonFrame(f1)
sub.pack(side=LEFT, expand=YES, fill=BOTH)
sub2 = RedSubFrame(f1)
sub2.pack(side=LEFT, expand=YES, fill=BOTH)
sub3 = ButtonFrame(sub2)
sub3.pack(padx=20, pady=20)
sub4 = RedSubFrame(f1)
sub4.pack(fill=BOTH, expand=YES)
cons = LoggingConsole(sub4)
cons.pack(fill=BOTH, expand=YES)


root.mainloop()
