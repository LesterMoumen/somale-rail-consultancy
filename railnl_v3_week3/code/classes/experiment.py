import csv
import matplotlib.pyplot as plt
from code.classes import helper_functions as helper
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.visualisation import Visualisation
from code.classes.traject import Traject

class Experiment():
    """ This Class handles each instance of an experiment by creating train
    trajects, running them, and evaluating their quality. Specific algorithms
    must inherit from this class to define the start location (e.g. randomly),
    how to select the next station (e.g. randomly or greedy) or to change the
    movement and run.
    """
    def __init__(self, connections_file, stations_file, number_of_trajects, max_time):
        """ Initializes the experiment.

        Input:
        - connections_file: csv file containing train connections
        - locations_file: csv file containing station locations (coordinates)
        - number_of_trajects: int, amount of trajects to be generated
        - max_time: int, the maximum amount of minutes allowed per train route
        """
        # Load csv files into dictionaries holding Connection and Station objects
        self.stations_dict, self.connections_dict = self.load_data(connections_file, stations_file)
        self.max_time = max_time
        self.number_of_trajects = number_of_trajects

        # List of colors for visualizing different trajecs
        self.color_list = ["blue", "orange", "green", "red", "purple",
                            "brown", "pink", "gray", "olive", "cyan",
                            "yellow", "violet", "indigo", "magenta", "teal",
                            "turquoise", "lime", "navy", "gold", "silver"]

        # List to store traject_objects of each train route
        self.traject_list = []

        # Create set of all connections
        self.connections_set = self.get_all_connections(connections_file)


    def load_data(self, connections_file, stations_file):
        """ Loads csv files of connection and location data into input
        connections and locations files into Station class. Returns dictionary
        with station/connection name as key, and Station/Connection object as
        value.
        """
        # Get cleaned up data from csv files
        clean_stations_data = helper.file_import(stations_file)
        clean_connections_data = helper.file_import(connections_file)

        # Create and add Station obects to stations_dict
        stations_dict = {}
        for station_data in clean_stations_data:
            station, y, x = station_data
            # Station object created with empty connection dictionary
            # Note: connection dictionaries will be filled later
            stations_dict[station] = Station(station, {}, (float(x), float(y)))

        # Create and add Connection objects to connection dict
        connections_dict = {}
        for connection_data in clean_connections_data:
            station1, station2, time_between_stations = connection_data
            connection_key = helper.sorted_connection(station1, station2)
            connections_dict[connection_key] = Connection(station1, station2, time_between_stations)

            # Add connection to relevant Station objects
            stations_dict[station1].connections[station2] = int(float(time_between_stations))
            stations_dict[station2].connections[station1] = int(float(time_between_stations))

        return stations_dict, connections_dict


    def calculate_quality(self, connection_histories = None, total_time = None):
        """ Calculate the (current) quality of the train trajects table. When
        called with connection_histories and total_time, it gives the current
        qualty and p. When called without, it will give the quality of the final
        train table.

        The formula: K = p*10000 - (T*100 + Min)
        - K is the quality (kwaliteit) of the train table
        - p is the fraction of visited connections
        - T is the number of trajects
        - Min is the total travel time in minutes
        """
        if connection_histories is None:
            connection_histories = self.get_connection_histories()
        if total_time is None:
            total_time = self.get_total_time()

        p = len(connection_histories) / len(self.connections_set)
        T = self.number_of_trajects
        quality = p * 10000 - (T*100 + total_time)

        return quality, p


    def valid_connection_options(self, traject_object):
        """ Returns dictionary of valid connection options: connections that can
        be reached from the current location within the max_time. The output
        format of the dict is {connecting station : time_to_station}.
        """
        # Get dictionary of connection options with respective time
        current_location = traject_object.location
        connection_options = self.stations_dict[current_location].connections

        # Get dictionary of connection options that are within time limit
        valid_connections = {}
        for connection, time in connection_options.items():
            real_time = traject_object.traject_time + time
            if real_time <= self.max_time:
                valid_connections[connection] = time

        return valid_connections


    def get_station_histories(self):
        """ Returns list of lists with station histories of each traject.
        """
        station_histories = []
        for traject in self.traject_list:
            station_histories.append(traject.station_history)

        return station_histories


    def get_connection_histories(self):
        """ Returns set of all connections visited.
        """
        connection_histories = set()
        for traject in self.traject_list:
            connection_histories = connection_histories.union(set(traject.connection_history))

        return connection_histories


    def get_all_connections(self, connections_file):
        """ Returns set with all connections from input csv file.
        """
        # Get cleaned up data from input file
        clean_connections = helper.file_import(connections_file)

        connections_set = set()
        for connection in clean_connections:
            station1, station2, time = connection
            connections_set.add(helper.sorted_connection(station1, station2))

        return connections_set


    def get_total_time(self):
        """ Returns the total time of all trains/trajects.
        """
        total_time = 0
        for traject in self.traject_list:
            total_time += traject.traject_time

        return total_time


    def reset_connection_frequencies(self):
        """ Resets all connection counts.
        """
        for connection, connection_object in self.connections_dict.items():
            connection_object.times_used = 0


    def initialize_trajects(self):
        """ Initializes a new traject object and adds to traject_list.
        Note: uses the start_station() function from inherited algoritm Class.
        This can for example be a random start location.
        """
        for i in range(self.number_of_trajects):
            start_location = self.start_station(list(self.stations_dict.keys()))
            self.traject_list.append(Traject(start_location, self.color_list[i]))


    def movement(self, traject_object):
        """ Moves train to next valid connecting station.
        Note: uses the select_next_station() from inherited algoritm Class. This
        can for example be a random next station.
        """
        valid_connections = self.valid_connection_options(traject_object)
        next_station = self.select_next_station(valid_connections)

        # Finishes traject when there are no next station options
        if next_station is None:
            traject_object.finished = True
        else:
            connection = helper.sorted_connection(traject_object.location, next_station)
            connection_time = self.connections_dict[connection].time
            traject_object.update(connection, next_station, connection_time)
            # Updates the amount the connection is used by one
            self.connections_dict[connection].update_used()

    def run_trajects(self):
        """ Runs trajects/trains until they are finished (reach max_minutes).
        """
        for traject_object in self.traject_list:
            # Loop until traject is finished
            while not traject_object.finished:
                self.movement(traject_object)


    def run(self):
        """ Run the experiment by initializing trajects and then running them.
        """
        self.initialize_trajects()
        self.run_trajects()


    def run_till_solution(self, max_iterations=10000):
        """ Runs experiment until a complete solution is found (p = 1).
        """
        p = 0
        iteration = 0

        while p != 1 and iteration <= max_iterations:
            iteration += 1
            self.traject_list = []
            self.initialize_trajects()
            self.reset_connection_frequencies()
            self.run_trajects()
            K, p = self.calculate_quality()

        return self


    def is_solution(self):
        """ Check if the experiment has reached a complete solution (p = 1).
        """
        K, p = self.calculate_quality()

        return p == 1


    def print_output(self):
        """ Prints traject and quality scores directly in terminal.
        """
        print("train, stations")
        for i, traject in enumerate(self.traject_list):
            print(f'train {i+1} {traject.station_history}')
        print("score", self.calculate_quality()[0])


    def output_to_csv(self, filename):
        """ Saves trajects and quality score to csv file.
        """
        with open(filename, 'w', newline = '') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['train', 'stations'])

            for i, traject in enumerate(self.traject_list):
                train = f"Train {i+1}"
                route = [traject.station_history]
                time = traject.traject_time
                csv_writer.writerow([train, route, time])

            total_quality, p = self.calculate_quality()
            csv_writer.writerow(["Score", total_quality])


    def visualisation(self, filename):
        """ Creates and saves the visualisation for the trajects and the train
        table and displays it. Uses the Visualisation class.
        """
        visualize = Visualisation(self.stations_dict, self.connections_dict, self.traject_list)
        # visualize.show_visualisation()
        visualize.save_visualisation(filename)
