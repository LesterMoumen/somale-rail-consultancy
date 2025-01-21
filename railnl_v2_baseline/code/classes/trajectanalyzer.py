

class TrajectAnalyzer():
    def __init__(self, stations_dict, connections_dict=None, traject_histories=None):
        """ To do: implement mechanism to update the list with used connections.
        """
        self.stations_dict = stations_dict

        #self.get_used_connections = self.find_odd_connections(traject_histories)

        self.dead_ends = self.find_dead_ends()
        self.odd_connections = self.find_odd_connections()

        # note: not implemented yet:
        #self.valid_connections = self.find_valid_connections(location, traject_time, max_time)

        self.next_start_location = self.find_next_start_location()

    def find_used_connections(self, traject_histories):
        """ Find used connections from traject_histories.
        """
        used_connections = {}
        for traject in traject_histories:
            for connection in traject.connection_history:
                print(connection)

    def find_dead_ends(self):
        """ Find dead-end stations: stations with only a single connection.
        Return list with dead_end stations.
        Output format: {station_name : [next_station, distance_to_next_station]}
        """
        dead_ends = {}
        # Loops over station object dictionary
        for station_name, station in self.stations_dict.items():
            if len(station.connections) == 1:
                next_station, time = ((list(station.connections.items())[0]))
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
            number_of_odd_connections = len(station.connections)
            # Check for odd number
            if number_of_odd_connections % 2 != 0:
                odd_connections[station_name] = number_of_odd_connections

        return odd_connections


    def find_valid_connection(self, location, traject_time, max_time):
        """
        To do: integrate into train_table.py
        Returns dictionary of valid connection options with respective time.
        Output format: {station : time}
        # e.g. self.location = "Den Helder", connection_options = {Alkmaar : 37}
        """
        # Get dictionary of connection options with respective time
        connection_options = self.stations_dict[location].connections

        # Get dictionary of connection options that are within time limit
        valid_connections = {}
        for connection, time in connection_options.items():
            real_time = traject_time + int(float(time))
            if real_time <= max_time:
                valid_connections[connection] = time

        return valid_connections


    def find_next_start_location(self):
        """ Find optimal starting location for next train/traject. """
        if self.dead_ends:
            # get dead_end with longest time and return as starting location
            next_start = max(self.dead_ends, key = self.dead_ends.get)
            return next_start

        elif self.odd_connections:
            # get odd_connection with most connections and return as starting location
            next_start = max(self.odd_connections, key = self.odd_connections.get)
            return next_start

        else:
            # to do: implement
            print("No dead end or odd connection station available to start from.")
