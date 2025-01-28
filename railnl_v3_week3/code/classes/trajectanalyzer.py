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
        self.used_stations = self.find_used_stations()

        #self.next_start_location = self.find_next_start_location()

    def find_used_stations(self):
        """ Find used station from station_histories in Traject2 class
        """
        used_stations = set()
        for traject in self.traject_list:
            for station in traject.station_history:
                used_stations.add(station)

        return used_stations

    def find_used_connections(self):
        """ Find used connections from traject_histories.
        """
        used_connections = set()
        for traject in self.traject_list:
            for connection in traject.connection_history:
                used_connections.add(connection)

        return used_connections

    def find_number_of_connections(self, station_object):
        """ Find number of connections for a single station.
        """
        connecting_stations = station_object.connections
        number_of_connections = 0
        connections_list = []
        for connecting_station in connecting_stations:
            if connecting_station not in self.used_connections:
                number_of_connections += 1
                connections_list.append(helper.sorted_connection(connecting_station, station_object.name))

        return number_of_connections, connections_list

    def find_dead_ends(self):
        """ Find dead-end stations: stations with only a single connection.
        Return list with dead_end stations.
        Output format: {station_name : [next_station, distance_to_next_station]}
        """
        dead_ends = {}

        self.used_connections = self.find_used_connections()
        # Loops over station object dictionary
        for station_name, station_object in self.stations_dict.items():
            number_of_connections, connections_list = self.find_number_of_connections(station_object)
            if number_of_connections == 1:

                if connections_list[0] not in self.used_connections:
                    time = self.connections_dict[connections_list[0]].time


                    dead_ends[station_name] = int(float(time))

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

                # Checks if connection not used yet
                if connection not in self.used_connections:
                    number_of_connections += 1

            # Check for odd number
            if number_of_connections % 2 != 0:
                odd_connections[station_name] = number_of_connections

        return odd_connections
        

    def find_next_start_location(self):
        """ Find optimal starting location for next train/traject. """
        dead_ends = self.find_dead_ends()
        odd_connections = self.find_odd_connections()


        if dead_ends:
            # get dead_end with longest time and return as starting location
            next_start = max(dead_ends, key = dead_ends.get)

        elif odd_connections:
            # get odd_connection with most connections and return as starting location
            next_start = max(odd_connections, key = odd_connections.get)

        else:
            # Pick a random station
            available = self.connections_set - self.used_connections
            next_start = random.choice(list(available))

        return next_start
