import matplotlib.pyplot as plt

class Visualisation():
    ''' Handles visualisation of train table.
    '''
    def __init__(self, stations_dict, connections_dict, traject_list):
        self.stations_dict = stations_dict
        self.connections_dict = connections_dict
        self.traject_list = traject_list


    def stations_plot(self):
        ''' Create a plot for the stations as a scatter plot
        '''
        x, y = [], []

        for station, station_object in self.stations_dict.items():
            x_coordinate, y_coordinate = station_object.coordinates

            y.append(y_coordinate), x.append(x_coordinate)

        # Plotting stations/cities
        plt.scatter(x, y)

    def plot_connection(self, connection_object, color, line_style = "-", line_width = 1, label=None):
        station1, station2 = connection_object.station1, connection_object.station2

        x1, y1 = self.stations_dict[station1].coordinates
        x2, y2 = self.stations_dict[station2].coordinates

        plt.plot([x1, x2], [y1, y2], color, linestyle=line_style, linewidth=line_width, label=None)


    def connection_frequency_plot(self):
        """
        """
        for connection, connection_object in self.connections_dict.items():
            frequency = connection_object.times_used

            # Plot the connections pair and its frequency how often a connecion has been used
            # How bigger the line_width how more frequent the connection has been used.
            if frequency > 1:
                self.plot_connection(connection_object, color="black", line_style="--", line_width=frequency)

                #     for connection_pair, coordinates in connections_plotted.items():
                #         frequency = connection_counts.get(connection_pair)
                #         line_width = frequency + 1
                #         plt.plot(coordinates[0], coordinates[1], '--k', linewidth = line_width


    # def connection_frequency_plot(self):
    #     '''
    #     Creates the connections between the stations with its frequency.
    #     '''
    #     # keeps track how often a connection has been used in traject_histories
    #     connection_counts = {}
    #     # keep track on the plotted connections as connection_pair; [x_station, x_connection, y_station, y_connection]
    #     connections_plotted = {}
    #
    #     for traject in self.traject_list:
    #         for index in range(len(traject.station_history)):
    #             current_station, next_station = traject[index].split('_')
    #             connection_pair = tuple(sorted((current_station, next_station)))
    #             connection_counts[connection_pair] = connection_counts.get(connection_pair, 0) + 1
    #
    #     for station, station_object in self.stations_dict.items():
    #         for connection in station_object.connections:
    #
    #             # make a tuple of the station and its connection and sort it alphabetically.
    #             connection_pair = tuple(sorted((station, connection)))
    #
    #             if connection_pair not in connections_plotted:
    #
    #                 x = [float(self.stations_dict[station].x_coordinate) , float(self.stations_dict[connection].x_coordinate)]
    #                 y = [float(self.stations_dict[station].y_coordinate), float(self.stations_dict[connection].y_coordinate)]
    #
    #                 connections_plotted[connection_pair] = [x,y]
    #
    #     # Plot the connections pair and its frequency how often a connecion has been used
    #     # how bigger the line_width how more frequent the connection has been used.
    #     for connection_pair, coordinates in connections_plotted.items():
    #         frequency = connection_counts.get(connection_pair)
    #         line_width = frequency + 1
    #         plt.plot(coordinates[0], coordinates[1], '--k', linewidth = line_width )


    def route_plot(self):
        '''
        Create the plot for each train traject
        '''
        train_count = 0
        for traject in self.traject_list:
            train_count += 1
            for connection in traject.connection_history:
                self.plot_connection(self.connections_dict[connection], color = traject.color,
                                     label = f'Train {train_count}')



                                    #if index == 0 else ""

    #
    #     for i, traject in enumerate(self.traject_histories):
    #         x_city = []
    #         y_city = []
    #
    #         # goes over the index in the traject list
    #         for index in range(len(traject)):
    #             current_station, next_station = traject[index].split('_')
    #
    #             x_city.append(stations_coordinates[current_station]['x'])
    #             y_city.append(stations_coordinates[current_station]['y'])
    #             x_city.append(stations_coordinates[next_station]['x'])
    #             y_city.append(stations_coordinates[next_station]['y'])
    #
    #             # plots the train route and only adds a label for the first point in the traject
    #             plt.plot(x_city, y_city, color = color_list[i], label=f'Train {i+1}' if index == 0 else "")
    #
    #             # clear the list so there will not be connections which do not exist due to overlapping points
    #             x_city.clear()
    #             y_city.clear()
    #
    #         plt.legend(loc = "lower right")


    def show_visualisation(self):
        ''' Combines the different plots in a single one, and shows it.
        '''
        self.stations_plot()
        self.connection_frequency_plot()
        self.route_plot()
        plt.title("Train trajects Holland visualized")
        # plt.axis('off')
        # plt.legend(loc = "lower right")

        plt.show()
