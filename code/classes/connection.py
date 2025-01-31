
from . import helper_functions as helper

class Connection():
    """ This class handles each Connection object. It serves as data storage
    container for the connection, while keeping track of how many times it is
    used.
    """
    def __init__(self, station1, station2, time):
        """ Initializes the Connection.

        Input:
        - station1: str, station name
        - station2: str, station name
        - time: int, the time in minutes between both stations
        """
        self.station1 = station1
        self.station2 = station2
        self.time = time

        # The amount of times the connection has been used
        self.times_used = 0

    def update_used(self):
        """ Updates the times_used counter by adding 1.
        """
        self.times_used += 1
