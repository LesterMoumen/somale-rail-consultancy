
class Station():
    """ Handles each station object.
    """
    def __init__(self, station, connections, x, y):
        self.name = station
        self.x_coordinate = x
        self.y_coordinate = y

        # Dictionary with connection options + connection time
        self.connections = connections
