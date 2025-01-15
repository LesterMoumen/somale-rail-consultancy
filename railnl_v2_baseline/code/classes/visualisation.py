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

        return stations_coordinates

    def connection_plot(self):
        '''
        Creates the connections in between the stations.
        '''
        connection_lines = []
        for connection, time in self.connections.items():
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
            plt.plot(connection[0], connection[1], 'k')


    def route_plot(self):
        '''
        Create the plot for each train traject
        '''
        stations_coordinates = self.stations_plot()

        for i, traject in enumerate(self.trajects):
            marked_cities = {}
            y_city = []
            x_city = []
            for station in traject:
                for city, coordinates in stations_coordinates.items():
                    if station == city:
                        marked_cities[city] = coordinates

            for city_went, coordinates in marked_cities.items():
                y_city.append(coordinates["y"])
                x_city.append(coordinates["x"])

            plt.plot(x_city,y_city, "--b")

    def show_visualisation(self):
        '''
        Combines the different plots in a single one
        '''
        self.stations_plot()
        self.connection_plot()
        self.route_plot()
        plt.show()
