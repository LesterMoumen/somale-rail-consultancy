import matplotlib.pyplot as plt

class Visualisation():
    ''' Handles visualisation of train table.
    '''
    def __init__(self, stations_dict, traject_histories):
        self.stations_dict = stations_dict
        self.traject_histories = traject_histories


    def stations_plot(self):
        ''' Create a plot for the stations as a scatter plot
        '''
        y = []
        x = []
        stations_coordinates = {}
        for station, station_object in self.stations_dict.items():
            y_coordinate_station = float(station_object.y_coordinate)
            x_coordinate_station = float(station_object.x_coordinate)

            # stations_coordinates[city] = {"x": x_coordinate, "y": y_coordinate}
            stations_coordinates[station] = {"x": x_coordinate_station, "y": y_coordinate_station}

            y.append(y_coordinate_station)
            x.append(x_coordinate_station)

        # Plotting stations/cities
        plt.scatter(x, y)

        return stations_coordinates


    def connection_plot(self):
        ''' Creates the connections in between the stations.
        '''
        connection_lines = []
        # keep track on the plotted connections in a set so there will not be any duplicate connections
        connections_plotted = set()

        for station, station_object in self.stations_dict.items():
            for connection in station_object.connections:

                # make a tuple of the station and its connection and sort it alphabetically.
                connection_pair = tuple(sorted((station, connection)))

                if connection_pair not in connections_plotted:
                    # print(connection)
                    x = []
                    y = []

                    x.append(float(self.stations_dict[station].x_coordinate))
                    y.append(float(self.stations_dict[station].y_coordinate))
                    x.append(float(self.stations_dict[connection].x_coordinate))
                    y.append(float(self.stations_dict[connection].y_coordinate))

                    connection_lines.append([x,y])
                    connections_plotted.add(connection_pair)

        # Plot connections between stations
        labelx = True
        for connection_coordinates in connection_lines:
            plt.plot(connection_coordinates[0], connection_coordinates[1], '--k', label="Empty routes" if labelx else "")
            labelx = False


    def route_plot(self):
        '''
        Create the plot for each train traject
        '''
        stations_coordinates = self.stations_plot()

        color_list = ["blue", "orange", "green", "red", "purple",
                      "brown", "pink", "gray", "olive", "cyran"]

        for i, traject in enumerate(self.traject_histories):
            x_city = []
            y_city = []

            # goes over the index in the traject list
            for index in range(len(traject)-1):
                current_station, next_station = traject[index].split('_')

                x_city.append(stations_coordinates[current_station]['x'])
                y_city.append(stations_coordinates[current_station]['y'])
                x_city.append(stations_coordinates[next_station]['x'])
                y_city.append(stations_coordinates[next_station]['y'])

                # plots the train route and only adds a label for the first point in the traject
                plt.plot(x_city, y_city, color = color_list[i], label=f'Train {i+1}' if index == 0 else "")

                # clear the list so there will not be connections which do not exist due to overlapping points
                x_city.clear()
                y_city.clear()

            plt.legend(loc = "lower right")


    def show_visualisation(self):
        ''' Combines the different plots in a single one, and shows it.
        '''
        self.stations_plot()
        self.connection_plot()
        self.route_plot()
        plt.title("Train trajects Holland visualized")

        plt.show()
