
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
        self._performance = [0 for _ in range(num_years)]

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
        Note that t is currently unused, but will be changed in the future.
        """
        assert(size is not None or performance is not None)
        assert(t > 0)

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


