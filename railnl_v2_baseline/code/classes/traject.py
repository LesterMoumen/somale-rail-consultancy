# baseline version
from code.algorithms.randomise import random_select_next_station
import random

class Traject():
    """ Handles a single train route/traject.
    """
    def __init__(self, start_location, stations, color, max_time):
        self.location = start_location # current station
        self.color = color # color of the traject
        self.connection_history = [] # list with connections visited
        self.traject_time = 0 # minutes traveled
        self.stations = stations # list of initialized station classes
        self.max_time = max_time # max time in minutes
        self.finished = False # initiate track as unfinished
        self.station_history = [start_location] # list with stations visited

    def valid_connection_options(self):
        # Get dictionary of connection options with respective time
        # Output format: {station : time, station : time, station : time}
        # e.g. self.location = "Den Helder", connection_options = {Alkmaar : 37}
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

        # Note:
        # Old code, kept here for reference, can be deleted upon checking.
        #def movement(self):
        #""" Random movement from current station to randomly chosen station from
        #the available connections. For the baseline model this is random, future
        #models will use more advanced algortihms to create more optimal time
        #tables.
        #TODO:
        #- clean up int(float(time))?
        #"""
        #valid_connections = self.valid_connection_options()

        # Checks if there are valid connections left, otherwise marks track as finished
        #if not valid_connections:
        #    self.finished = True
        #else:
        #    # Randomly pick next connection from valid options
        #    next_station = random.choice(list(valid_connections.keys()))
        #
            # Add connection to history, and sort alphabetically
        #    connection = sorted([self.location, next_station])
        #    self.connection_history.append(connection[0] + "_" + connection[1])

            # update self.time and self.location
        #    self.traject_time += int(float(valid_connections[next_station]))
        #    self.location = next_station
        #
        # Create list for connections that are within time limit
        #possible_connections = []
        #
        # To avoid passing the maximum time per track, append all stations within time limit to a new list
        #for connection, time in connection_options.items():
        #    real_time = self.traject_time + int(float(time)) # Maybe a nicer solution than using int(float) to prevent errors?
        #    if real_time <= self.max_time:
        #        possible_connections.append((connection, time))
        #
        # If len(list) > 1 exercize random
        #if len(possible_connections) > 1:
        #    next_connection, time = random.choice(possible_connections)
        #
        #    # Split connections into stations
        #    split_location = next_connection.split("_")
        #    # Check if currently at same station
        #    if split_location[0] != self.location:
        #        next_station = split_location[0]
        #    else:
        #        next_station = split_location[1]
        #
        #    self.traject_history.append(next_station)
        #    self.location = next_station
        #    self.traject_time += int(float(time)) # Maybe a nicer solution than using int(float) to prevent errors?
        #    self.connection_history.append(next_connection)
        #
        # If len(list) == 1, take this as next movement
        #elif len(possible_connections) == 1:
        #    next_connection, time = possible_connections[0]
        #
        #    # Split connections into stations
        #    split_location = next_connection.split("_")
        #    # Check if currently at same station
        #    if split_location[0] != self.location:
        #        next_station = split_location[0]
        #    else:
        #        next_station = split_location[1]
        #
        #    self.traject_history.append(next_station)
        #    self.location = next_station
        #    self.traject_time += int(float(time)) # Maybe a nicer solution than using int(float) to prevent errors?
        #    self.connection_history.append(next_connection)

        # If list is empty, track is finished
        #else:
        #    self.finished = True

    def run(self):
        """ Move the train until track is finished. Track is finished if
        the next traject would cause the traject to exceed the maximum allowed time.
        """
        while not self.finished:
            self.movement()

        return self.station_history, self.connection_history, self.traject_time
