import code.classes.helper_functions as helper
import random

class TrajectAnalyzer():
    def __init__(self, stations_dict, connections_dict, traject_list, connections_set):
        """ To do: implement mechanism to update the list with used connections.
        """
        self.stations_dict = stations_dict
        self.connections_dict = connections_dict
        self.traject_list = traject_list
        self.connections_set = connections_set

        self.used_connections = self.find_used_connections()

        self.dead_ends = self.find_dead_ends()
        self.odd_connections = self.find_odd_connections()

        self.next_start_location = self.find_next_start_location()

    def find_used_connections(self):
        """ Find used connections from traject_histories.
        """
        used_connections = set()
        for traject in self.traject_list:
            for connection in traject.connection_history:
                used_connections.add(connection)

        return used_connections

    def find_dead_ends(self):
        """ Find dead-end stations: stations with only a single connection.
        Return list with dead_end stations.
        Output format: {station_name : [next_station, distance_to_next_station]}
        """
        dead_ends = {}
        # Loops over station object dictionary
        for station, station_object in self.stations_dict.items():
            if len(station_object.connections) == 1:
                next_station, time = ((list(station_object.connections.items())[0]))

                # Checks if connection already used
                if helper.sorted_connection(station, next_station) in self.used_connections:
                        break

                dead_ends[station] = int(float(time))

        return dead_ends


    def find_odd_connections(self):
        """ Find stations with odd number of connections. Returns dictionary
        with stations and number of odd connections.
        Output format: {station : number_of_odd_connections}
        # e.g. {"Den Helder" : 1} # just connected to Alkmaar
        """
        odd_connections = {}
        for station_name, station in self.stations_dict.items():
            number_of_connections = 0
            for connection, time in station.connections.items():

                # Checks if connection already used
                if connection in self.used_connections:
                        break

                number_of_connections += 1

            # Check for odd number
            if number_of_connections % 2 != 0:
                odd_connections[station_name] = number_of_connections

        return odd_connections


    def find_next_start_location(self):
        """ Find optimal starting location for next train/traject. """
        if self.dead_ends:
            # get dead_end with longest time and return as starting location
            next_start = max(self.dead_ends, key = self.dead_ends.get)

        elif self.odd_connections:
            # get odd_connection with most connections and return as starting location
            next_start = max(self.odd_connections, key = self.odd_connections.get)

        else:
            # Pick a random station
            available = self.connections_set - self.used_connections
            next_start = random.choice(list(available))

        return next_start
