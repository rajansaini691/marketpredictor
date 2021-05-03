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

        # size[t], performance[t], age[t] gives the product's size/performance/age at year t
        self._size = [size for _ in range(num_years)]
        self._performance = [performance for _ in range(num_years)]
        self._age = list(range(num_years))      # Goes from 0 ==> num_years - 1

        # Is the product actually in production?
        self._alive = True

        # The simulation's current year
        self._year = 0

    def update_time(self, t):
        """
        Change the product's current point in time        
        """
        self._year = t
        pub.sendMessage(f"product_changed/{self._name}", name=self._name, coords=(self._performance[t], self._size[t]), age=self._age[t], time=self._year, time_change=True)

    def update_stats(self, t, size=None, performance=None, age=None):
        """
        Update the size, performance, and age past the provided year t.
        """
        assert(size is not None or performance is not None)

        if t is None:
            t = self._year

        assert(t >= 0)

        if size is not None:
            self._size[t:] = len(self._size[t:]) * [size]

        if performance is not None:
            self._performance[t:] = len(self._performance[t:]) * [performance]

        if age is not None:
            self._age[t:] = [age + i for i in range(num_years - t)]
            assert(len(self._age) == len(self._performance))
            assert(self._age[t] == age)
            assert(t < num_years - 1 and self._age[t+1] == age + 1)

        assert(len(self._size) == len(self._performance))

        # Broadcast that the model changed (views should listen for this)
        # TODO Abstract out params to a namedtuple (call it ProductEvent or something)
        pub.sendMessage(f"product_changed/{self._name}", name=self._name, coords=(self._performance[t], self._size[t]), age=self._age[t], time=t, time_change=False)

    # TODO Get rid of these methods and write a method that returns a ProductEvent namedtuple
    #      that gives all of the relevant stats (name, performance, size, age, etc) at a given time t
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


