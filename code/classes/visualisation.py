import matplotlib.pyplot as plt

class Visualisation():
    """ This class handles the visualisation of the train table that is created
    through an experiment. The visualisation gives every traject their own
    color and shows overlap through black dashed lines that are thicker when the
    amount of overlap increases. Upon creating the visualisation, it can be
    displayed directly and/or saved as a file in the output map.
    """
    def __init__(self, stations_dict, connections_dict, traject_list):
        """ Initializes the Visualisation object.

        Input:
        - stations_dict: station names as key, Station objects as value
        - connections_dict: connection names as key, Connection objects as value
        - traject_list: with all Traject objects
        """
        self.stations_dict = stations_dict
        self.connections_dict = connections_dict
        self.traject_list = traject_list


    def get_all_station_coordinates(self):
        """ Get coordinates of all stations and returns as two lists (with x and
        y coordinates).
        """
        x_list, y_list = [], []

        # Get coordinates of stations and add to coordinate lists
        for station, station_object in self.stations_dict.items():
            x, y = station_object.coordinates
            x_list.append(x), y_list.append(y)

        return x_list, y_list


    def get_connection_coordinates(self, connection_object):
        """ Get coordinates of a single connection and return coordinates as two
        lists (with x and y coordinates).
        """
        station1, station2 = connection_object.station1, connection_object.station2
        x1, y1 = self.stations_dict[station1].coordinates
        x2, y2 = self.stations_dict[station2].coordinates

        return [x1, x2], [y1, y2]


    def plot_stations(self):
        """ Create scatter plot of all stations.
        """
        x_list, y_list = self.get_all_station_coordinates()

        # Zorder = 3 ensures station shows on top
        plt.scatter(x_list, y_list, zorder=3)


    def plot_connection(self, connection_object, color, line_style = "-", line_width = 1):
        """ Plot a connection between two stations.
        """
        x, y = self.get_connection_coordinates(connection_object)
        plt.plot(x, y, color, linestyle=line_style, linewidth=line_width)


    def plot_all_connections(self):
        """ Plots all connections as lightgray dashed lines. This function does
        not take into account whether the connection is used or not.
        """
        for connection, connection_object in self.connections_dict.items():
            self.plot_connection(connection_object, color="lightgray", line_style="--")


    def plot_connection_frequency(self):
        """ Plots connection frequency: the number of times that connection is
        used. It shows this through dashed lines that are thicker when the amount
        of overlap increases.
        """
        for connection, connection_object in self.connections_dict.items():
            frequency = connection_object.times_used
            if frequency > 1:
                self.plot_connection(connection_object, color="black", line_style="--", line_width=frequency)


    def route_plot(self):
        """ Plots the route of each traject with their respective color.
        """
        for traject in self.traject_list:
            for connection in traject.connection_history:
                self.plot_connection(self.connections_dict[connection], color = traject.color)


    def create_visualisation(self):
        """ Creates the visualisation of the train table by combining all plots.
        """
        plt.figure()
        self.plot_all_connections()
        self.route_plot()
        self.plot_connection_frequency()
        self.plot_stations()

        # Plots title including the total number of trajects
        plt.title(f"Train Table Visualised with {len(self.traject_list)} Trajects")

        # Leaves axis out as they are not required for the visualisation
        plt.axis('off')


    def show_visualisation(self):
        """ Shows the visualisation
        """
        self.create_visualisation()
        plt.show()

        # Close to save memory
        plt.close()


    def save_visualisation(self, filename=None):
        """ Saves the visualisation.
        """
        self.create_visualisation()

        # If no filename provided, use default
        if not filename:
            filename = "unnamed_train_table_visualisation.png"

        # Save visualisation as png
        plt.savefig(filename, format='png')
        print(f"Visualisation saved as {filename}")

        # CLose to save memory
        plt.close()
