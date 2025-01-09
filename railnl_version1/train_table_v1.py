# Malve Rail Consulting
# 07/01/2025
#
# First version of the main code for making the train tables (de lijnvoering).
# It randomly creates the trajects of the train table (routes) with a given max
# time limit.

import csv
import helper_functions as helper
import random
import itertools

class Traject():
    """ Handles a single train route/traject.
    """
    def __init__(self, start_location, connections, locations, connections_options, color, max_time):
        self.location = start_location # current station
        self.color = color
        self.traject_history = [] # list with stations visited
        self.connection_history = [] # list with connections visited
        self.traject_time = 0 # minutes traveled
        self.connections = connections
        self.connections_options = connections_options
        self.locations = locations
        self.max_time = max_time # max time in minutes

    def movement(self):
        """ Random movement from current station to randomly chosen station from
        the available connections. For the baseline model this is random, future
        models will use more advanced algortihms to create more optimal time
        tables.
        """
        # Makes list of connecting stations with connecting times
        connection_options = list(self.connections_options[self.location].items())

        next_connection, time  = random.choice(connection_options)

        split_location = next_connection.split("_")
        if split_location[0] != self.location:
            next_station = split_location[0]
        else:
            next_station = split_location[1]

        self.traject_history.append(next_station)
        self.connection_history.append(next_connection)
        self.location = next_station
        self.traject_time += int(float(time)) # Maybe a nicer solution that using int(float) to prevent errors?

    def run(self):
        """ Move the train until exceeding the max_time.
        To do: make the <= max_time apply to the total time, not the n-1 total
        time as it currently only stops once the max time has been passed.
        """
        while self.traject_time <= self.max_time:
            self.movement()

        return self.traject_history, self.connection_history, self.traject_time


class Train_table():
    """ Handles and creates multiple trajects. Calculates cost of created table
    and outputs findings.
    """
    def __init__(self, connections, locations, number_of_trajects, max_time):
        self.connections = helper.connections_dict(connections)
        self.connections_options = helper.connecting_options_dict(connections)
        self.locations = helper.locations_dict(locations)
        self.trajects_list = [] # list to store trajects
        self.add_trajects(number_of_trajects, max_time)
        self.traject_histories = []
        self.connection_histories = []
        self.total_time = 0

    def create_table(self):
        """ Creates the train table.
        """
        for traject in self.trajects_list:
            traject_history, connection_history, traject_time = traject.run()
            self.traject_histories.append(traject_history)
            self.connection_histories.append(connection_history)
            self.total_time += traject_time

    def add_trajects(self, number_of_trajects, max_time):
        """ Add new trains/trajects.
        """
        color_list = ["blue", "orange", "green", "red", "purple",
                      "brown", "pink", "gray", "olive", "cyran"]

        for i in range(number_of_trajects):
            start_location = random.choice(list(self.locations.keys()))

            self.trajects_list.append(Traject(start_location, self.connections, self.locations, self.connections_options, color_list[i], max_time))

    def calculate_quality(self):
        """ Calculate the quality of the train table. Optimal is 10000.
        formula:     K = p*10000 - (T*100 + Min)
        waarin K de kwaliteit van de lijnvoering is, p de fractie van de bereden verbindingen
        (dus tussen 0 en 1), T het aantal trajecten en Min het aantal minuten in alle trajecten samen.

        """
        print()
        # Create set with all stations in region
        all_connections = set(self.connections.keys())

        # Merge traject_histories list of lists into single set
        visited_connections = set()
        for list in self.connection_histories:
            visited_connections = visited_connections.union(set(list))

        # Calculate fraction (p) of visited connections
        p = len(visited_connections) / len(all_connections)

        # Get total number of trajects (T)
        T = len(self.trajects_list)

        # Calculate cost
        quality = p * 10000 - (T*100 + self.total_time)

        return quality

    def print_output(self):
        """ Prints the output, see the assignment on ah.proglab.nl/cases/railnl
        for the correct format. For now, just prints the traject_histories.
        """
        print("train, stations")
        for i, traject in enumerate(self.traject_histories):
            # print()
            print(traject)
        print("score", self.calculate_quality())

    def output_to_csv(self):
        """ Returns output as csv file.
        """
        csv_file = open('train_stations.csv', 'w', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['train', 'stations'])

        for i, traject in enumerate(self.traject_histories):
            # print(f"train {i+1}, {traject}")
            train = f"train {1+i}"

            csv_writer.writerow([train, traject])
        csv_writer.writerow(["score", self.calculate_quality()])
        csv_file.close()

    def visualisation(self):
        """ To do: making it create a plot with trajects. See visualisatie_v1.py.
        """
        None
# class Visualisation():
#     def __init__(self, )
# 

# Input files
locations = "StationsHolland_locaties.csv"
connections = "ConnectiesHolland.csv"

if __name__ == "__main__":
    baseline_train_table = Train_table(connections, locations, 7, max_time = 120)
    baseline_train_table.create_table()
    # Prints the established trajects
    baseline_train_table.print_output()
    #print(baseline_train_table.calculate_quality())
    baseline_train_table.output_to_csv()
