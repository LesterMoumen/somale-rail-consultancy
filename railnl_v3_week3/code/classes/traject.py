

class Traject():
    """ This class handles a single train route/traject. It keeps track of the
    movement history and movement time.
    """
    def __init__(self, start_location, color):
        """ Initializes the Traject.

        Input:
        - start_location: str, the first station of the traject
        - color: str, the color that will be used to visualize this traject with
        """
        self.location = start_location
        self.color = color

        # Total time traveled
        self.traject_time = 0

        # Lists with connections and stations visited
        self.connection_history = []
        self.station_history = [start_location]

        # Indicates whether this traject has not reached max time yet
        # While False, this traject can still move
        self.finished = False


    def update(self, new_connection, new_start_station, new_time):
        """ Updates the traject after moving to the next station.
        """
        self.location = new_start_station
        self.connection_history.append(new_connection)
        self.station_history.append(new_start_station)
        self.traject_time += int(float(new_time))
