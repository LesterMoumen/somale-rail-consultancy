import csv
import matplotlib.pyplot as plt
from code.classes import helper_functions as helper
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.visualisation import Visualisation
from code.classes.traject2 import Traject2

class Experiment():
    """
    """
    def __init__(self, connections_file, locations_file, number_of_trajects, max_time):
        self.stations_dict, self.connections_dict = self.load_data(connections_file, locations_file)
        self.max_time = max_time
        self.number_of_trajects = number_of_trajects

        self.color_list = ["blue", "orange", "green", "red", "purple",
        "brown", "pink", "gray", "olive", "cyan",
        "yellow", "violet", "indigo", "magenta", "teal",
        "turquoise", "lime", "navy", "gold", "silver"]

        self.traject_list = []

        self.connections_set = self.get_all_connections(connections_file)


    def load_data(self, connections_file, locations_file):
        """ Loads input connections and locations files into Station class.
        Returns dictionary with station name as key, and station object as value.
        To do: edit dit, maakt nu ook connections_dict
        """
        clean_locations = helper.file_import(locations_file)
        clean_connections = helper.file_import(connections_file)

        # Create and add Station obects to stations_dict
        stations_dict = {}
        for location in clean_locations:
            station, y, x = location
            # Station crreated with empty connection dictionary, being appended in line 52/53
            stations_dict[station] = Station(station, {}, (float(x), float(y)))

        # Create and add Connection objects to connection dict
        connections_dict = {}
        for connection in clean_connections:
            station1, station2, time = connection
            sorted_key = sorted([station1, station2])
            connections_dict[(sorted_key[0] + "_" + sorted_key[1])] = Connection(station1, station2, time)

            # Add connection to Station objects
            stations_dict[station1].connections[station2] = time
            stations_dict[station2].connections[station1] = time

        return stations_dict, connections_dict

    def calculate_quality(self):
        """ Calculate the quality of the train table. Optimal is 10000.
        formula:     K = p*10000 - (T*100 + Min)
        waarin K de kwaliteit van de lijnvoering is, p de fractie van de bereden verbindingen
        (dus tussen 0 en 1), T het aantal trajecten en Min het aantal minuten in alle trajecten samen.
        """

        # Calculate fraction (p) of visited connections
        p = len(self.get_connection_histories()) / len(self.connections_set)
        # Get total number of trajects (T)
        T = len(self.traject_list)
        # Calculate cost
        quality = p * 10000 - (T*100 + total_time)
        print(f"Total Quality (Score): {quality}, Fraction of Visited Connections (p): {p}, time {total_time}")

        return quality, p


    def valid_connection_options(self, traject_object):
        """ Gives dictionary of valid connection options with respective time.
        Output format: {station : time, station : time, station : time}
        # e.g. self.location = "Den Helder", connection_options = {Alkmaar : 37}
        """
        # Get dictionary of connection options with respective time
        location = traject_object.location
        connection_options = self.stations_dict[location].connections

        # Get dictionary of connection options that are within time limit
        valid_connections = {}
        for connection, time in connection_options.items():
            real_time = traject_object.traject_time + int(float(time))
            if real_time <= self.max_time:
                valid_connections[connection] = time

        return valid_connections

    def get_station_histories(self):
        """ Get a list of lists with station histories of each traject.
        """
        station_histories = []
        for traject in self.traject_list:
            station_histories.append(traject.station_history)

        return station_histories

    def get_connection_histories(self):
        """ Get a set of all connections visited.
        """
        connection_histories = set()
        for traject in self.traject_list:
            connection_histories = connection_histories.union(set(traject.connection_history))

        return connection_histories

    def get_all_connections(self, connections_file):
        """ Get a set with all connections.
        """
        connections_set = set()
        clean_connections = helper.file_import(connections_file)

        for connection in clean_connections:
            station1, station2, time = connection
            # Sort stations alphabetically
            sorted_stations = sorted([station1, station2])
            connections_set.add(sorted_stations[0] + "_" + sorted_stations[1])

        return connections_set

    def get_total_time(self):
        total_time = 0
        for traject in self.traject_list:
            total_time += traject.traject_time

        return total_time

    def initialize_trajects(self):
        """ Add new trains/trajects.
        """
        for i in range(self.number_of_trajects):
            start_location = self.start_station(list(self.stations_dict.keys()))

            self.traject_list.append(Traject2(start_location, self.color_list[i])) #, max_time, select_next_station_algoritm))

    def movement(self, traject_object):
        """ To do: Move to experiment with (self, next_station)
        """
        valid_connections = self.valid_connection_options(traject_object)
        next_station = self.select_next_station(valid_connections)

        if next_station is None:
            traject_object.finished = True

        else:
            connection = f"{sorted([traject_object.location, next_station])[0]}_{sorted([traject_object.location, next_station])[1]}"
            time = self.connections_dict[connection].time
            traject_object.update(connection, next_station, time)

            # Update times ued
            self.connections_dict[connection].update_used()

    def run_trajects(self):
        """ Move to next station.
        """
        for traject_object in self.traject_list:
            # Loop until traject is finished (finished when runs out of options within the 120 minutes)
            while not traject_object.finished:
                self.movement(traject_object)

    def run(self):
        """ Run the experiment.
        """
        self.initialize_trajects()
        self.run_trajects()


    def reset_connection_frequencies(self):
        """ Resets dictionary for iterations.
        """
        for connection, connection_object in self.connections_dict.items():
            connection_object.times_used = 0


    def run_till_solution(self, max_iterations=10000):
        """ Runs experiment until a complete solution is found (p = 1)
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

        # print(K)
        # print(iteration)
        return self


    def is_solution(self):
        """ Check if the experiment is a complete solution (p = 1). """
        _, p = self.calculate_quality()
        return p == 1


    def print_output(self):
        """ Prints in terminal as ouput the trajects and quality score. Mainly used for
        debugging. Final version of code will only use output_to_csv().
        """
        print("train, stations")
        for i, traject in enumerate(self.traject_list):
            print(f'train {i+1} {traject.station_history}')
        print("score", self.calculate_quality()[0])


    def output_to_csv(self, filename):
        """
        Returns output as csv file.

        Note: does not work yet! See print_output() for how station_histories
        is replaced by traject.station_history
        """
        csv_file = open(filename, 'w', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['train', 'stations'])

        for i, traject in enumerate(self.traject_list):
            train = f"train {1+i}"
            csv_writer.writerow([train, traject.station_history, traject.traject_time])

        csv_writer.writerow(["score", self.calculate_quality()])
        csv_file.close()

    def visualisation(self, filename):
        """
        Creates the visualisation for the trains and the train table and displays it.
        """
        visualize = Visualisation(self.stations_dict, self.connections_dict, self.traject_list)
        visualize.show_visualisation()
        # visualize.save_visualisation(filename)

        #  # Save the visualisation to a PNG file
        # plt.savefig(filename, format='png')
        # print(f"Visualization saved as {filename}")
