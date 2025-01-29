import code.classes.helper_functions as helper
import random

class TrajectAnalyzer():
    """ This class analyzes the train trajects/routes and provides information
    about:
    - used stations
    - used connections
    - dead ends: stations with only a single (unnused) connection)
    - odd connections: stations with odd connections
    - start station: the most optimal place to start the next traject
    """
    def __init__(self, stations_dict, connections_dict, traject_list, connections_set):
        """ Initializes the TrajectAnalyzer.

        Input:
        - stations_dict: station names as key, Station objects as value
        - connections_dict: connection names as key, Connection objects as value
        - traject_list: with all Traject objects
        - connections_set:
        """
        self.stations_dict = stations_dict
        self.connections_dict = connections_dict
        self.traject_list = traject_list
        self.connections_set = connections_set
        self.used_connections = self.find_used_connections()

    def find_used_stations(self):
        """ Find all used station from station_histories in Traject class.
        """
        used_stations = set()
        for traject in self.traject_list:
            for station in traject.station_history:
                used_stations.add(station)

        return used_stations


    def find_used_connections(self):
        """ Finds all connections that have been visited in the trajects and
        return as set.
        """
        used_connections = set()
        for traject in self.traject_list:
            for connection in traject.connection_history:
                used_connections.add(connection)

        return used_connections


    def find_number_of_connections(self, station_object):
        """ Finds the number of connections for a single station that have not
        been visited/used yet. Returns the number and a list of unnused
        connections.
        """
        # Get connections of current station (used and unnused ones)
        connecting_stations = station_object.connections

        number_of_connections = 0
        connections_list = []
        for connecting_station in connecting_stations:
            connection = helper.sorted_connection(connecting_station, station_object.name)

            # When connection is unnused, add connection to list and increase count
            if connection not in self.used_connections:
                number_of_connections += 1
                connections_list.append(connection)

        return number_of_connections, connections_list


    def find_dead_ends(self):
        """ Finds dead-end stations: stations with only a single (unused)
        connection. Returns dictionary with dead end station as key and
        connecting time as value.
        """
        dead_ends = {}
        for station_name, station_object in self.stations_dict.items():
            number_of_connections, connections_list = self.find_number_of_connections(station_object)
            if number_of_connections == 1:

                # When connection is unnused, add connection with time to dict
                if connections_list[0] not in self.used_connections:
                    time = self.connections_dict[connections_list[0]].time
                    dead_ends[station_name] = int(float(time))

        return dead_ends


    def find_odd_connections(self):
        """ Finds stations with odd number of (unused) connections. Returns
        dictionary with stations and number of odd connections.
        """
        odd_connections = {}
        for station_name, station_object in self.stations_dict.items():
            number_of_connections, connections_list = self.find_number_of_connections(station_object)

            # When number of connection is odd, add to dictionary
            if number_of_connections % 2 != 0:
                odd_connections[station_name] = number_of_connections

        return odd_connections


    def find_next_start_location(self):
        """ Find optimal starting location for next train/traject. Optimal is
        defined here as follows:

        1. Dead end station with longest connecting time. When a dead end is
        selected, the function will return the only possible connection too.

        2. Station with the largest number of odd connections.

        3. When 1 and 2 are not possible, a random station will be used that has
        used connections available.
        """
        # Find all dead end stations and stations with odd number of connections
        dead_ends = self.find_dead_ends()
        odd_connections = self.find_odd_connections()

        # Set default as None because it only applies to dead ends
        next_start_connection = None

        # If there are stations with a dead end, the station with the longest
        # starting location will be chosen.
        if dead_ends:
            next_start = max(dead_ends, key = dead_ends.get)
            # Connecting time from dead_end station to connceting station
            time = dead_ends[next_start]

            # Find the only possible connection by looping through connections
            # of the station to find the connecting station that matches the time
            for connecting_station, connection_time in self.stations_dict[next_start].connections.items():
                if int(float(connection_time)) == time:
                    next_start_connection = (connecting_station, time)

        # If there are stations with odd connections, the station with the
        # largest number of odd connections will be chosen as starting location.
        elif odd_connections:
            next_start = max(odd_connections, key = odd_connections.get)

        # If no dead ends or odd connections, random station is chosen
        else:
            # Pick a random station
            available = self.connections_set - self.used_connections
            next_start = random.choice(list(available))

        return next_start, next_start_connection
