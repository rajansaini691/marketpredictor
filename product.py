from pubsub import pub
import tkinter as tk
from tkinter import ttk

"""
Message Passing API:
    product_changed/{name}      Product has changed somehow. Its coordinates,
                                name, and time must be sent so that the view
                                can render it.

    changing_time               UI-generated event telling all products to change
                                their time
                                Just need the time

    product_changing            UI-generated event telling a single product to
                                change a specific stat or stats. 
                                name is required, as is at least one of size
                                and performance. Passing None for time changes
                                a stat at the product's current time.
    """

class Product:
    """
    A product has a name, size, performance, and year.
    """
    def __init__(self, name: str, size: float, performance: float,
                 year:int=None, num_years=None):
        """
        Note that num_years is the total number of years in the simulation (I think 6)
        """
        # Product name; string
        self._name = name

        # size[t], performance[t] gives the product's size/performance at year t
        self._size = [size for _ in range(num_years)]
        self._performance = [performance for _ in range(num_years)]

        # Is the product actually in production?
        self._alive = True

        # The simulation's current year
        self._year = 0

    def update_time(self, t):
        """
        Change the product's current point in time        
        """
        self._year = t
        pub.sendMessage(f"product_changed/{self._name}", name=self._name, coords=(self._performance[t], self._size[t]), time=self._year)

    def update_stats(self, t, size=None, performance=None):
        """
        Update the size and performance past the provided year t.
        """
        assert(size is not None or performance is not None)

        if t is None:
            t = self._year

        assert(t >= 0)

        if size is not None:
            self._size[t:] = len(self._size[t:]) * [size]

        if performance is not None:
            self._performance[t:] = len(self._performance[t:]) * [performance]

        assert(len(self._size) == len(self._performance))

        
        # TODO Send name, curr_coords, (in future) customer score
        pub.sendMessage(f"product_changed/{self._name}", name=self._name, coords=(self._performance[t], self._size[t]), time=t)

    def get_performance(self, t=None):
        """
        Return either the performance in the current year or at a desired year
        """
        return self._performance[t] if t is not None else self._performance[self._year]

    def get_size(self, t=None):
        """
        Return either the size in the current year or at a desired year
        """
        return self._size[t] if t is not None else self._size[self._year]

# This is a View()
class ProductPlot:
    """
    Draws a Product to a given matplotlib axis
    """
    def __init__(self, ax, canvas, product):
        """
        Parameters:
            ax          The axis on which this stuff will be drawn
            product     A Product object
        """
        # Lets us refresh canvas when something changes
        self._canvas = canvas

        # TODO We may not even need to store a copy of this guy
        self._product = product

        initial_size = product.get_size()
        initial_performance = product.get_performance()

        # Draw coordinate
        self._product_coord = ax.scatter(initial_size, initial_performance)

        # ax.scatter automatically assigns each spot a new color,
        # so this guarantees that our colors will be unique
        self._color = self._product_coord.get_edgecolor()

        # Add text
        self._name = ax.text(initial_size, initial_performance, product._name)

        pub.subscribe(self._change_product, f"product_changed/{product._name}")

    # FIXME Handle case when product_changed_stats updates
    # stats outside of the current time.
    def _change_product(self, name, time, coords):
        """
        Draw the name and product coordinate
        """
        s,p = coords

        # Update coordinate positioning
        self._product_coord.set_offsets((s, p))
        self._name.set_position((s, p))

        self._canvas.draw()


# This is a view
class ProductGUI:
    """
    Takes care of the GUI elements that allow user to modify location of products.
    Renders them and generates user events.
    """
    def __init__(self, parent, products):
        """
        Parameters:
            parent          TK object to draw input boxes on
            products        A list of Products to make inputs for
                            (this class does not modify them, just uses
                            them for initialization)
        """
        # TODO Get things side-by-side
        for p in products:
            # Add label
            tk.Label(parent, text=p._name).pack()

            # Add input stuff
            product_perf = tk.DoubleVar(value=p.get_performance())
            product_size = tk.DoubleVar(value=p.get_size())
            product_input_perf = ttk.Entry(parent, textvariable=product_perf)
            product_input_size = ttk.Entry(parent, textvariable=product_size)
            product_input_perf.pack()
            product_input_size.pack()

            product_input_perf.bind('<Key-Return>',
                lambda _: self._on_update_performance(p._name, product_perf))
            product_input_size.bind('<Key-Return>',
                lambda _: self._on_update_size(p._name, product_size))

    def _on_update_performance(self, name, var):
        """
        Parameters:
            name        Name of the product to update
            var         The DoubleVar containing the data
        """
        pub.sendMessage("product_changing", name=name, performance=var.get())

    def _on_update_size(self, name, var):
        """
        Parameters:
            name        Name of the product to update
            var         The DoubleVar containing the data
        """
        pub.sendMessage("product_changing", name=name, size=var.get())


# This is a controller
class ProductController:
    """
    This should be the only thing talking to the tkinter window
    and modifying the model. Acts as a mediator between views and products.
    """
    def __init__(self, axis, canvas, products, parent):
        """
        Listens for user input events (like updating the time) and
        changes state of the given products accordingly 
        """
        # Index products by name for better lookups
        self._products = {p._name: p for p in products}

        # ProductPlot objects act as a view for products that render them
        # to an axis. They should not modify the products.
        self._product_plots = [ProductPlot(axis, canvas, p) for p in products]

        # Enables modification of the product
        self._product_gui = ProductGUI(parent, products)

        pub.subscribe(self._change_stats, 'product_changing')
        pub.subscribe(self._change_time, 'changing_time')

    def _change_stats(self, name, time=None, size=None, performance=None):
        assert(size is not None or performance is not None)
        assert(name is not None)

        p = self._products[name]
        p.update_stats(time, size=size, performance=performance)

    def _change_time(self, time):
        for n in self._products:
            p = self._products[n]
            p.update_time(time)
            
