# baseline version
from code.algorithms.randomise import random_select_next_station
import random

class Traject():
    """ Handles a single train route/traject.
    """
    def __init__(self, start_location, stations, color, max_time, select_next_station_algoritm):
        self.location = start_location # current station
        self.color = color # color of the traject
        self.connection_history = [] # list with connections visited
        self.traject_time = 0 # minutes traveled
        self.stations = stations # list of initialized station classes
        self.max_time = max_time # max time in minutes
        self.finished = False # initiate track as unfinished
        self.station_history = [start_location] # list with stations visited
        self.select_next_station_algoritm = select_next_station_algoritm


    def valid_connection_options(self):
        """ Gives dictionary of valid connection options with respective time.
        Output format: {station : time, station : time, station : time}
        # e.g. self.location = "Den Helder", connection_options = {Alkmaar : 37}
        """
        # Get dictionary of connection options with respective time
        connection_options = self.stations[self.location].connections

        # Get dictionary of connection options that are within time limit
        valid_connections = {}
        for connection, time in connection_options.items():
            real_time = self.traject_time + int(float(time))
            if real_time <= self.max_time:
                valid_connections[connection] = time

        return valid_connections


    def movement(self):
        """ Move to next station.
        """
        valid_connections = self.valid_connection_options()
        next_station = random_select_next_station(valid_connections)

        if next_station is None:
            self.finished = True
            return

        # Add connection to history, and sort alphabetically
        connection = sorted([self.location, next_station])
        self.connection_history.append(connection[0] + "_" + connection[1])

        # update self.time and self.location
        self.traject_time += int(float(valid_connections[next_station]))
        self.location = next_station
        self.station_history.append(next_station)


    def run(self):
        """ Move the train until track is finished. Track is finished if
        the next traject would cause the traject to exceed the maximum allowed time.
        """
        while not self.finished:
            self.movement()

        return self.station_history, self.connection_history, self.traject_time
