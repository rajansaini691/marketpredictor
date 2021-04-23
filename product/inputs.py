import tkinter as tk
from tkinter import ttk
from pubsub import pub

product_name_font = ("Arial", 14)
attr_label_font = ("Arial", 9)

# This is a view
class ProductGUI:
    """
    Renders inputs needed to modify a single product and generates
    user events
    """
    # TODO  Add a param that provides row, and a class responsible for
    #       positioning these guys
    def __init__(self, parent, name, initial_size, initial_performance):
        """
        Parameters:
            parent                  TK object to draw input boxes on
            name                    Product name
            initial_size            Initial value in text box
            initial_performance     Initial value in text box
        """
        # Top-level thing letting us organize stuff
        self._frame = tk.Frame(parent)

        # Add label
        self._label = tk.Label(self._frame, text=name, font=product_name_font)
        self._perf_label = tk.Label(
                self._frame, text="performance", font=attr_label_font)
        self._size_label = tk.Label(
                self._frame, text="size", font=attr_label_font)
        self._name = name

        # Add input stuff
        self._perf_var = tk.DoubleVar(value=initial_performance)
        self._size_var = tk.DoubleVar(value=initial_size)
        self._perf_input = ttk.Entry(self._frame, textvariable=self._perf_var)
        self._size_input = ttk.Entry(self._frame, textvariable=self._size_var)

        self._perf_input.bind('<Key-Return>', self._on_update_performance)
        self._size_input.bind('<Key-Return>', self._on_update_size)

        # Put stuff onto the GUI
        self.show()

    def show(self):
        # Pack things within frame
        self._label.pack()
        self._perf_label.pack()
        self._perf_input.pack()
        self._size_label.pack()
        self._size_input.pack()

        # Frames are horizontally-aligned
        self._frame.pack(side=tk.LEFT)

    def _on_update_performance(self, _):
        """
        Callback for when parameter gets updated
        """
        try:
            p = self._perf_var.get()
            n = self._name
            pub.sendMessage("product_changing", name=n, performance=p)
        except:
            print("Don't enter non-numbers, please")

    def _on_update_size(self, name, var):
        """
        Callback for when parameter gets updated
        """
        try:
            s = self._size_var.get()
            n = self._name
            pub.sendMessage("product_changing", name=n, size=s)
        except:
            print("Don't enter non-numbers, please")


