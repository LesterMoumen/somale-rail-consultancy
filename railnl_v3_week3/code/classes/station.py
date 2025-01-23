
class Station():
    """ Handles each station object.
    """
    def __init__(self, station, connections, coordinates):
        self.name = station
        self.coordinates = coordinates

        # Dictionary with connection options + connection time
        self.connections = connections
