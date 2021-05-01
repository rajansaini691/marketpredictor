
import matplotlib.pyplot as plt
from collections import namedtuple
from matplotlib.transforms import Affine2D, ScaledTranslation, offset_copy

Age = namedtuple('Age', ['mean', 'stdev', 'importance'])
Price = namedtuple('Price', ['low', 'high', 'importance'])
Position = namedtuple('Position', ['importance'])
MTBF = namedtuple('MTBF', ['low', 'high', 'importance'])
BuyingCriteria = namedtuple('BuyingCriteria', ['age', 'price', 'position', 'mtbf'])

class MarketSegment:
    def __init__(self, starting_point, offset, drift, customer_criteria, name):
        """
        Defines a new industry segment

        Parameters:
            starting_point      (performance, size)
            offset              An (x,y) tuple denoting the optimal point offset
            drift               An (x,y) tuple denoting the drift
            customer_criteria   A BuyingCriteria class with the info used in
                                this segment (see Conditions Report)
            name                A string providing the market segment's name
        """
        self._starting_point = starting_point
        self._offset = offset
        self._drift = drift
        self._name = name
        self._criteria = customer_criteria

        # Sanity check
        should_be_one = (self._criteria.age.importance
            + self._criteria.price.importance
            + self._criteria.position.importance
            + self._criteria.mtbf.importance)
        assert(abs(should_be_one - 1) < 0.0000001)


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

    def get_price_range(self, t):
        """
        Get the price at a given year t (decreases by 0.5 each year)
        returns (low, high)
        """
        return (self._criteria.price.low - .5*t, self._criteria.price.high - .5*t)
    
    def get_mtbf_range(self, t=0):
        """
        Get the mtbf range (doesn't change)
        returns (low, high)
        """
        return (self._criteria.mtbf.low, self._criteria.mtbf.high)


class MarketSegmentPlot:
    """
    Draws a MarketSegment's various parameters for use with matplotlib
    """
    def __init__(self, fig, ax, industry_segment):
        """
        Parameters:
            fig                 The figure on which this stuff will be drawn
            ax                  The axis on which this stuff will be drawn
            industry_segment    A MarketSegment object
        """
        self._industry_segment = industry_segment
        initial_centroid = industry_segment.get_location(0)
        x0, y0 = initial_centroid
        
        initial_ideal_spot = industry_segment.get_ideal_spot(0)

        # Draw ideal spot
        self._ideal_spot = ax.scatter(*initial_ideal_spot)

        # ax.scatter automatically assigns each spot a new color,
        # so this guarantees that our colors will be unique
        self._color, = self._ideal_spot.get_edgecolor()

        # Add a circle with radius 2.5 around the segment
        self._circle = plt.Circle(initial_centroid, 2.5, fill=False, color=self._color)
        ax.add_artist(self._circle)

        # Add text in the center of the circle
        self._name = ax.text(*initial_centroid, industry_segment._name,
                c=self._color, ha='center', va='center')

        # Add pricing info
        self._price_display_offset = (0, 0.5)   # Where should price be drawn?
        px, py = self._price_display_offset
        p_low, p_high = industry_segment.get_price_range(0)
        self._price = ax.text(x0 + px, y0 + py, f"\${p_low} to \${p_high}",
                c=self._color, ha='center', va='center')

        # Add mtbf info
        self._mtbf_display_offset = (0, -0.5)
        mx, my = self._mtbf_display_offset
        mtbf_low, mtbf_high = industry_segment.get_mtbf_range()
        self._mtbf = ax.text(x0 + mx, y0 + my, f"{mtbf_low} to {mtbf_high}",
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

        # Get locations
        new_centroid = self._industry_segment.get_location(int(t))
        x, y = new_centroid

        # Update circle
        self._circle.set_center((new_centroid))

        # Update name
        self._name.set_position(new_centroid)

        # Update price contents and location
        p_low, p_high = self._industry_segment.get_price_range(t)
        px, py = self._price_display_offset
        self._price.set_position((x + px, y + py))
        self._price.set_text(f"\${p_low} to \${p_high}")

        # Update mtbf location
        mtbf_low, mtbf_high = self._industry_segment.get_mtbf_range()
        mx, my = self._mtbf_display_offset
        self._mtbf.set_position((x + mx, y + my))
        self._mtbf.set_text(f"{mtbf_low} to {mtbf_high}")
