import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAGG")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk

# TODO Taken from tutorial
LARGE_FONT= ("Verdana", 12)

class MarketSegment:
    def __init__(self, starting_point, offset, drift, name):
        """
        Defines a new industry segment

        Parameters:
            starting_point      (performance, size)
            offset              An (x,y) tuple denoting the optimal point offset
            drift               An (x,y) tuple denoting the drift
            name                A string providing the market segment's name
        """
        self._starting_point = starting_point
        self._offset = offset
        self._drift = drift
        self._name = name

    def get_location(self, t):
        """
        Get the location at a given year t
        (Note: t is measured from start of simulation)
        """
        x0, y0 = self._starting_point
        dx, dy = self._drift
        return (x0 + dx * t, y0 + dy * t)

    def get_ideal_spot(self, t):
        """
        Get the ideal spot at a given year t
        (Note: t is measured from start of simulation)
        """
        x, y = self.get_location(t)
        dx, dy = self._offset
        return (x + dx, y + dy)


class MarketSegmentPlot:
    """
    Draws a MarketSegment's various parameters for use with matplotlib
    """
    def __init__(self, ax, industry_segment):
        """
        Parameters:
            ax                  The axis on which this stuff will be drawn
            industry_segment    A MarketSegment object
        """
        self._industry_segment = industry_segment
        
        initial_ideal_spot = industry_segment.get_ideal_spot(0)

        # Draw ideal spot
        self._ideal_spot = ax.scatter(*initial_ideal_spot)

        # ax.scatter automatically assigns each spot a new color,
        # so this guarantees that our colors will be unique
        self._color, = self._ideal_spot.get_edgecolor()

        # Add a circle with radius 2.5 around the segment
        initial_centroid = industry_segment.get_location(0)
        self._circle = plt.Circle(initial_centroid, 2.5, fill=False, color=self._color)
        ax.add_artist(self._circle)

        # Add text in the center of the circle
        self._name = ax.text(*initial_centroid, industry_segment._name)
        

    def update(self, t):
        """
        Draws the name, ideal spot, and bounding circle

        Parameters:
            t           Years from the start
        """
        # Update ideal spot
        new_ideal_spot = self._industry_segment.get_ideal_spot(int(t))
        self._ideal_spot.set_offsets(new_ideal_spot)

        # Update circle
        new_centroid = self._industry_segment.get_location(int(t))
        self._circle.set_center((new_centroid))

        # Update name
        self._name.set_position(new_centroid)
        


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
                command=lambda t: self.update_time(t, canvas, market_segment_plots))

        # Put the slider onto the window
        time_slider.pack()


    # TODO Rewrite completely (call update() on all children)
    def update_time(self, t, canvas, market_segment_plots):
        """
        Draw the market segments to the graph
        """
        for msp in market_segment_plots:
            msp.update(t)

        canvas.draw()


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


















