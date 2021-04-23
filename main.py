
from marketsegment import MarketSegment, MarketSegmentPlot
from product import Product, ProductPlot, ProductController

import matplotlib
matplotlib.use("TkAGG")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import numpy as np
from pubsub import pub


# TODO Figure out how to let time slider and products talk to each other
class PerceptualMap(tk.Frame):
    """
    Draw the perceptual map graph and the needed sliders

    Disclaimer:
        A lot of this code was taken from a tutorial and can likely
        be improved
    """
    def __init__(self, parent, controller, num_years, market_segments, products):
        tk.Frame.__init__(self, parent)

        # The actual graph
        f = Figure(figsize=(5,5), dpi=100)
        ax = f.add_subplot(111)
        ax.set_title("Perceptual Map Predictor")
        ax.set_xlim(0,20)       # Set graph limits
        ax.set_ylim(0,20)

        # Add line going through 3 ideal points
        # y = m*(x - x0) + y0
        x0,y0 = 2.5-0.8, 17.5+0.8
        x1,y1 = 7.5+1.4, 12.5-1.4
        m = (y1-y0)/(x1-x0)
        lin, = ax.plot([0, y0-m*x0], [x0-y0/m, 0])

        # TODO Add line going through initial size segment and in-between ideal

        # Grid line
        ax.minorticks_on()
        ax.grid(b=True, which='minor')
        ax.grid(b=True, which='major')

        # Use MarketSegmentPlot objects to draw each market segment
        market_segment_plots = [MarketSegmentPlot(ax, ms) for ms in market_segments]

        # Hooks the graph up to the window somehow
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Allows the user to move around the graph
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()

        # Calling pack() places an object onto the window, I think
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Allows the user to choose the point in time
        time_slider = tk.Scale(self,
                from_=0, to=num_years-1, resolution=1, orient=tk.HORIZONTAL,
                command=lambda t: self.update_time(int(t), canvas, market_segment_plots),
                length=300)

        # Put the slider onto the window
        time_slider.pack()

        # This thing deals with products
        self._pg = ProductController(ax, canvas, products, self)

        
    def update_time(self, t, canvas, market_segment_plots):
        """
        Draw the market segments to the graph
        """
        # TODO Listen to event instead
        for msp in market_segment_plots:
            msp.update(t)
        
        pub.sendMessage("changing_time", time=t)

        canvas.draw()

    
class Window(tk.Tk):
    """
    Configure the actual window.

    Disclaimer:
        A lot of this code was taken from a tutorial and can likely
        be improved
    """
    def __init__(self, num_years, market_segments, products, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Set the window title
        tk.Tk.wm_title(self, "Perceptual Map Predictor")
        
        # Ensure contents fit to window. No idea how this works :)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Draw the perceptual map
        self.frame = PerceptualMap(container, self, num_years, market_segments, products)
        self.frame.grid(row=0, column=0, sticky="nsew") # Something important


if __name__ == "__main__":
    # Constants
    NUM_YEARS = 10

    # Create segments
    traditional = MarketSegment(
            starting_point=(5, 15), offset=(0, 0), drift=(0.7, -0.7),
            name="Traditional")
    low_end = MarketSegment(
            starting_point=(2.5, 17.5), offset=(-0.8, 0.8), drift=(0.5, -0.5),
            name="Low End")
    performance = MarketSegment(
            starting_point=(8, 17), offset=(1.4, -1.0), drift=(1.0, -0.7),
            name="Performance")
    high_end = MarketSegment(
            starting_point=(7.5, 12.5), offset=(1.4, -1.4), drift=(0.9, -0.9),
            name="High End")
    size = MarketSegment(
            starting_point=(3, 12), offset=(1.0, -1.4), drift=(0.7, -1.0),
            name="Size")

    market_segments = [low_end, traditional, high_end, performance, size]

    # Create products
    test = Product("test", 5, 5, 0, num_years=NUM_YEARS)
    idk = Product("idk", 2, 2, 0, num_years=NUM_YEARS)

    products = [test, idk]
    
    # GUI code
    app = Window(NUM_YEARS, market_segments, products)
    app.mainloop()
