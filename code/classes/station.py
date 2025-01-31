class Station():
    """ This class handles each station object. It serves as data storage
    container for the station.
    """
    def __init__(self, station, connections, coordinates):
        """ Initializes the Station object.

        Input:
        - station: str, station name
        - connections: dict, connection options as key, connection time as value
        - coordinates: tuple, with x and y coordinate (floats)
        """
        self.name = station
        self.coordinates = coordinates
        self.connections = connections
