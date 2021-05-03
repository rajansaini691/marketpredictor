from pubsub import pub

# This is a View()
class ProductPlot:
    """
    Draws a Product to a given matplotlib axis
    """
    # TODO Accept a single namedtuple containing the data rather than a list of attributes
    def __init__(self, ax, canvas, name, initial_size, initial_performance):
        """
        Parameters:
            ax                      The axis on which this stuff will be drawn
            canvas                  The canvas on which this stuff will be drawn
            name                    The product's name
            initial_size            The product's initial position
            initial_performance     The product's initial position
        """
        # Lets us refresh canvas when something changes
        self._canvas = canvas

        # Draw coordinate
        self._product_coord = ax.scatter(initial_performance, initial_size, c='#000')

        # ax.scatter automatically assigns each spot a new color,
        # so this guarantees that our colors will be unique
        self._color = self._product_coord.get_edgecolor()

        # Add name+age label (with age of zero). For ex: "cake (0)"
        self._name_label = ax.text(initial_performance, initial_size, f"{name} (0)")
        self._product_name = name

        pub.subscribe(self._change_product, f"product_changed/{name}")

    # FIXME draw() should be called once per time change and once per
    #       product change, pretty laggy rn
    def _change_product(self, name, time, coords, age, time_change):
        """
        Draw the name and product coordinate
        """
        p,s = coords

        # Update coordinate positioning
        self._product_coord.set_offsets((p, s))
        self._name_label.set_position((p, s))
        self._name_label.set_text(f"{name} ({age})")

        # If the time has changed, lots of points will get redrawn,
        # so no need to redraw the entire canvas
        if time_change is not True:
            self._canvas.draw()
