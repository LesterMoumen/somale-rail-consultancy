# Malve Rail Consulting
# 10/01/2025
#
# First version of the main code for making the train tables (de lijnvoering).
# It randomly creates the trajects of the train table (routes) with a given max
# time limit.

import csv
import helper_functions as helper
import random
import matplotlib.pyplot as plt
import itertools

class Traject():
    """ Handles a single train route/traject.
    """
    def __init__(self, start_location, connections, locations, connections_options, color, max_time):
        self.location = start_location # current station
        self.color = color # color of the traject
        self.traject_history = [] # list with stations visited
        self.connection_history = [] # list with connections visited
        self.traject_time = 0 # minutes traveled
        self.connections = connections
        self.connections_options = connections_options
        self.locations = locations
        self.max_time = max_time # max time in minutes
        self.finished = False # initiate track as unfinished

    def movement(self):
        """ Random movement from current station to randomly chosen station from
        the available connections. For the baseline model this is random, future
        models will use more advanced algortihms to create more optimal time
        tables.
        TODO:
        - a lot of duplicate code, we will clean this up in either an object
        or just cleaner code.
        - clean up int(float(time))
        """
        # Makes list of connecting stations with connecting times
        connection_options = list(self.connections_options[self.location].items())
        # Create list for connections that are within time limit
        possible_connections = []

        # To avoid passing the maximum time per track, append all stations within time limit to a new list
        for connection, time in connection_options:
            real_time = self.traject_time + int(float(time)) # Maybe a nicer solution than using int(float) to prevent errors?
            if real_time <= self.max_time:
                possible_connections.append((connection, time))

        # If len(list) > 1 exercize random
        if len(possible_connections) > 1:
            next_connection, time = random.choice(possible_connections)

            # Split connections into stations
            split_location = next_connection.split("_")
            # Check if currently at same station
            if split_location[0] != self.location:
                next_station = split_location[0]
            else:
                next_station = split_location[1]

            self.traject_history.append(next_station)
            self.location = next_station
            self.traject_time += int(float(time)) # Maybe a nicer solution than using int(float) to prevent errors?
            self.connection_history.append(next_connection)

        # If len(list) == 1, take this as next movement
        elif len(possible_connections) == 1:
            next_connection, time = possible_connections[0]

            # Split connections into stations
            split_location = next_connection.split("_")
            # Check if currently at same station
            if split_location[0] != self.location:
                next_station = split_location[0]
            else:
                next_station = split_location[1]

            self.traject_history.append(next_station)
            self.location = next_station
            self.traject_time += int(float(time)) # Maybe a nicer solution than using int(float) to prevent errors?
            self.connection_history.append(next_connection)

        # If list is empty, track is finished
        else:
            self.finished = True

    def run(self):
        """ Move the train until track is finished. Track is finished if
        the next traject would cause the traject to exceed the maximum allowed time.
        """
        while not self.finished:
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
        """ Prints in terminal as ouput the trajects and quality score. Mainly used for
        debugging. Final version of code will only use output_to_csv().
        """
        print("train, stations")
        for i, traject in enumerate(self.traject_histories):
            # print()
            print(traject)
        print("score", self.calculate_quality())

    def output_to_csv(self):
        """
        Returns output as csv file.
        """
        csv_file = open('train_stations.csv', 'w', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['train', 'stations'])

        for i, traject in enumerate(self.traject_histories):
            train = f"train {1+i}"
            csv_writer.writerow([train, traject])

        csv_writer.writerow(["score", self.calculate_quality()])
        csv_file.close()

    def visualisation(self):
        """
        Creates the visualisation for the trains and the train table and displays it.
        """
        visualize = Visualisation(self.connections, self.locations, self.traject_histories)
        visualize.show_visualisation()

class Visualisation():
    '''
    To do: all the functions need to use the same coordinates with self. So the plot uses
    the same points and the route will use the connecting lines.
    '''
    def __init__(self, connections, locations, trajects):
        self.connections = connections
        self.locations = locations
        self.trajects = trajects

    def stations_plot(self):
        '''
        Create a plot for the stations as a scatter plot
        '''
        y = []
        x = []
        stations_coordinates = {}
        for city, coordinates in self.locations.items():
            y_coordinate, x_coordinate = float(coordinates[0]), float(coordinates[1])

            stations_coordinates[city] = {"x": x_coordinate, "y": y_coordinate}
            y.append(y_coordinate)
            x.append(x_coordinate)

        # Plotting stations/cities
        plt.scatter(x, y)

        # self.stations_coordinates = stations_coordinates

        return stations_coordinates

    def connection_plot(self):
        '''
        Creates the connections in between the stations.
        '''
        connection_lines = []
        for connection, time in self.connections.items():
            # print(connection)
            x = []
            y = []

            # splitting the connection in 2 cities
            city1, city2 = connection.split("_")

            coordinates_city1 = self.locations[city1]
            coordinates_city2 = self.locations[city2]

            y.append(float(coordinates_city1[0]))
            x.append(float(coordinates_city1[1]))
            y.append(float(coordinates_city2[0]))
            x.append(float(coordinates_city2[1]))

            connection_lines.append([x,y])

        # Plot connections between stations
        for connection in connection_lines:
            plt.plot(connection[0], connection[1], '--k')


    def route_plot(self):
        '''
        Create the plot for each train traject
        '''
        stations_coordinates = self.stations_plot()

        color_list = ["blue", "orange", "green", "red", "purple",
                      "brown", "pink", "gray", "olive", "cyran"]

        for i, traject in enumerate(self.trajects):
            x_city = []
            y_city = []
            # goes over the index in the traject list
            for index in range(len(traject)-1):
                current_station = traject[index]
                next_station = traject[index + 1]

                x_city.append(stations_coordinates[current_station]['x'])
                y_city.append(stations_coordinates[current_station]['y'])
                x_city.append(stations_coordinates[next_station]['x'])
                y_city.append(stations_coordinates[next_station]['y'])

                # plots the train route and only adds a label for the first point in the traject
                plt.plot(x_city, y_city, color = color_list[i], label=f'Train {i+1}' if index == 0 else "")
                plt.legend()

    def show_visualisation(self):
        '''
        Combines the different plots in a single one
        '''
        self.stations_plot()
        self.connection_plot()
        self.route_plot()
        plt.show()


# Input files
locations = "StationsHolland_locaties.csv"
connections = "ConnectiesHolland.csv"

if __name__ == "__main__":
    # Create baseline model with 7 locations and 120 minutes max
    baseline_train_table = Train_table(connections, locations, 7, max_time = 120)
    baseline_train_table.create_table()

    # Printing output in terminal for debugging purposes
    baseline_train_table.print_output()

    baseline_train_table.output_to_csv()
    baseline_train_table.visualisation()
