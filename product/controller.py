from pubsub import pub
import tkinter as tk
from tkinter import ttk
from product.plot import ProductPlot
from product.inputs import ProductGUI

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
        self._product_plots = [ProductPlot(axis, canvas, p._name, p.get_size(),
                               p.get_performance()) for p in products]

        # Enables modification of the product
        self._product_menu = [ProductGUI(parent, p._name, p.get_size(),
                              p.get_performance()) for p in products]

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
            
