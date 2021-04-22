
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
        self._size = [0 for _ in range(num_years)]
        self._size[0] = size
        self._performance = [0 for _ in range(num_years)]
        self._performance[0] = performance

        # Is the product actually in production?
        self._alive = True

        # The simulation's current year
        self._year = 0

    def update_time(self, t):
        """
        Change the product's current point in time        
        """
        # TODO Change size and performance's indices
        self._year = t

    def update_stats(self, t, size=None, performance=None):
        """
        Update the size and performance for the provided year t.
        """
        assert(size is not None or performance is not None)
        assert(t >= 0)

        if size is not None:
            self._size[t] = size
        if performance is not None:
            self._performance[t] = performance

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

# TODO Implement
class ProductPlot:
    """
    Draws a Product to a given matplotlib axis
    """
    def __init__(self, ax, product):
        """
        Parameters:
            ax          The axis on which this stuff will be drawn
            product     A Product object
        """
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

    def update(self, t):
        """
        Draw the name and product coordinate
        """
        # Change the product's time
        self._product.update_time(t)

        # Update size and performance
        size = self._product.get_size()
        performance = self._product.get_performance()
        self._product_coord.set_offsets((size, performance))

        # Update name
        self._name.set_position(size, performance)

    # TODO There should be a better way to do this. Probably have ProductPlot
    # and Product be siblings owned by ProductGUI, rather than children->grandchildren. IDK, though
    def update_stats(self, t, size=None, performance=None):
        self._product.update_stats(t, size=size, performance=performance)

        # Update size and performance
        size = self._product.get_size()
        performance = self._product.get_performance()
        self._product_coord.set_offsets((size, performance))

        # Update name
        self._name.set_position((size, performance))


    def get_location(self):
        return (self._product.get_performance(), self._product.get_size())
