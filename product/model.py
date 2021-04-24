from pubsub import pub

class Product:
    """
    A product has a name, size, performance, and year.
    """
    def __init__(self, name: str, size: float, performance: float,
            mtbf:int, year:int=None, num_years=None):
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
        pub.sendMessage(f"product_changed/{self._name}", name=self._name, coords=(self._performance[t], self._size[t]), time=self._year, time_change=True)

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
        pub.sendMessage(f"product_changed/{self._name}", name=self._name, coords=(self._performance[t], self._size[t]), time=t, time_change=False)

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


