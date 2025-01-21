# baseline version

import random
import csv
from code.algorithms.randomise import random_start_station
from .traject import Traject
from .station import Station
from .visualisation import Visualisation
from .connection import Connection
from . import helper_functions as helper

class Train_table():
    """ Handles and creates multiple trajects. Calculates cost of created table
    and outputs findings.
    """
    def __init__(self, connections, locations, number_of_trajects, max_time, start_location_algorithm, select_next_station_algoritm):
        self.stations_dict, self.connections_dict = self.load_data(connections, locations)
        self.trajects_list = [] # list to store trajects
        self.add_trajects(number_of_trajects, max_time, start_location_algorithm, select_next_station_algoritm)
        self.connections_set = self.create_connections_set(connections) # set of connections
        self.traject_histories = []
        self.station_histories = []
        self.total_time = 0


    def load_data(self, connections, locations):
        """ Loads input connections and locations files into Station class.
        Returns dictionary with station name as key, and station object as value.
        To do: edit dit, maakt nu ook connections_dict
        """
        clean_locations = helper.file_import(locations)
        clean_connections = helper.file_import(connections)

        # Create and add Station obects to stations_dict
        stations_dict = {}
        for location in clean_locations:
            station, y, x = location
            stations_dict[station] = Station(station, {}, x, y)

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

    def create_table(self):
        """ Creates the train table (lijnvoering).
        """
        for traject in self.trajects_list:
            station_history, connection_history, traject_time = traject.run()
            self.traject_histories.append(connection_history)
            self.total_time += traject_time
            self.station_histories.append(station_history)


    def add_trajects(self, number_of_trajects, max_time, start_location_algorithm, select_next_station_algoritm):
        """ Add new trains/trajects.
        """
        color_list = ["blue", "orange", "green", "red", "purple",
                      "brown", "pink", "gray", "olive", "cyran"]

        for i in range(number_of_trajects):
            start_location = start_location_algorithm(list(self.stations_dict.keys()))
            self.trajects_list.append(Traject(start_location, self.stations_dict, color_list[i], max_time, select_next_station_algoritm))
            # start_location = random_start_station(list(self.stations_dict.keys()))
            # self.trajects_list.append(Traject(start_location, self.stations_dict, color_list[i], max_time))


    def create_connections_set(self, connections):
        """ Creates connections set with each connection pair alphabetically ordered.
        """
        connections_set = set()
        clean_connections = helper.file_import(connections)

        for connection in clean_connections:
            station1, station2, time = connection
            # Sort stations alphabetically
            sorted_stations = sorted([station1, station2])
            connections_set.add(sorted_stations[0] + "_" + sorted_stations[1])

        return connections_set

    def calculate_quality(self):
        """ Calculate the quality of the train table. Optimal is 10000.
        formula:     K = p*10000 - (T*100 + Min)
        waarin K de kwaliteit van de lijnvoering is, p de fractie van de bereden verbindingen
        (dus tussen 0 en 1), T het aantal trajecten en Min het aantal minuten in alle trajecten samen.
        """
        # Merge traject_histories list of lists into single set
        visited_connections = set()
        for list in self.traject_histories:
            visited_connections = visited_connections.union(set(list))

        # Calculate fraction (p) of visited connections
        p = len(visited_connections) / len(self.connections_set)
        # Get total number of trajects (T)
        T = len(self.trajects_list)
        # Calculate cost
        quality = p * 10000 - (T*100 + self.total_time)

        return quality


    def print_output(self):
        """ Prints in terminal as ouput the trajects and quality score. Mainly used for
        debugging. Final version of code will only use output_to_csv().
        """
        print("train, stations")
        for i, stations in enumerate(self.station_histories):
            print(f'train {i+1} {stations}')
        print("score", self.calculate_quality())


    def output_to_csv(self):
        """
        Returns output as csv file.
        """
        csv_file = open('output/train_stations.csv', 'w', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['train', 'stations'])

        for i, stations in enumerate(self.station_histories):
            train = f"train {1+i}"
            csv_writer.writerow([train, stations])

        csv_writer.writerow(["score", self.calculate_quality()])
        csv_file.close()


    def visualisation(self):
        """
        Creates the visualisation for the trains and the train table and displays it.
        """
        visualize = Visualisation(self.stations_dict, self.traject_histories)
        visualize.show_visualisation()
