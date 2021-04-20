
from marketsegment import MarketSegment, MarketSegmentPlot

import matplotlib
matplotlib.use("TkAGG")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import numpy as np


class PerceptualMap(tk.Frame):
    """
    Draw the perceptual map graph and the needed sliders

    Disclaimer:
        A lot of this code was taken from a tutorial and can likely
        be improved
    """
    def __init__(self, parent, controller, market_segments):
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

        # Add line going through initial size segment and in-between ideal
        #x0,y0 = 

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
                from_=0, to=10, resolution=1, orient=tk.HORIZONTAL,
                command=lambda t: self.update_time(int(t), canvas, market_segment_plots),
                length=300)

        # Put the slider onto the window
        time_slider.pack()


    def update_time(self, t, canvas, market_segment_plots):
        """
        Draw the market segments to the graph
        """
        for msp in market_segment_plots:
            msp.update(t)

        canvas.draw()


    # TODO Add entry boxes so we can use this function
    def update_point(self, ax, canvas, x=None, y=None):
        """
        Draw the desired point to the graph
        """
        assert(x is not None or y is not None)

        help(self._point)
        new_x, new_y = self._point

        if x is not None:
            new_x = x

        if y is not None:
            new_y = y

        self._point = (new_x, new_y)
        


class Window(tk.Tk):
    """
    Configure the actual window.

    Disclaimer:
        A lot of this code was taken from a tutorial and can likely
        be improved
    """
    def __init__(self, market_segments, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Set the window title
        tk.Tk.wm_title(self, "Perceptual Map Predictor")
        
        # Ensure contents fit to window. No idea how this works :)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Draw the perceptual map
        self.frame = PerceptualMap(container, self, market_segments)
        self.frame.grid(row=0, column=0, sticky="nsew") # Something important


if __name__ == "__main__":
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
    
    # GUI code
    app = Window(market_segments)
    app.mainloop()


















