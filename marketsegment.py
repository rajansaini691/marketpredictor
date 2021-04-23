
import matplotlib.pyplot as plt

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
        self._name = ax.text(*initial_centroid, industry_segment._name,
                c=self._color, ha='center', va='center')
        

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

