# Malve Rail Consulting
# 07/01/2025
#
# First version of the visualisation. Has to be put into functions and moved
# to train_table.py or helper_functions.py? Comments to be added.

import matplotlib.pyplot as plt
import csv
from helper_functions import file_import, connections_dict, locations_dict

def stations_plot(file):
    y = []
    x = []
    cities = {}
    with open(file) as locaties_file:
        lines = locaties_file.readlines()[1:]
        for line in lines:
            if line == "":
                continue
            split_data = line.split(",")

            city = str(split_data[0])
            y_coordinate = float(split_data[1])
            x_coordinate = float(split_data[2])

            cities[city] = {"y":y_coordinate, "x":x_coordinate}

            # coordinates for scatter
            y.append(y_coordinate)
            x.append(x_coordinate)

    # Plotting stations/cities
    for city, coordinates in cities.items():
        print(city)
        plt.scatter(x, y)
        plt.text(coordinates["x"]+.03, coordinates["y"]+.03, city, fontsize=9)
    return cities


def connection_plot(file):
    # Intialize connections dictionary
    connections = {}
    cities = stations_plot(stations)

    with open(file) as connecties_file:
        lines = connecties_file.readlines()[1:]
        for line in lines:
            line = line.strip()
            if line == "":
                continue
            split_data = line.split(",")

            city1 = split_data[0]
            city2 = split_data[1]

            coordinates_city1 = cities[city1]
            coordinates_city2 = cities[city2]

            connections[city1 + "-" + city2] = {city1:coordinates_city1, city2:coordinates_city2}

    # print(connections)
    connection_lines = []
    for connection, cities in connections.items():
        x = []
        y = []

        for city, coordinates in cities.items():
            x.append(coordinates["x"])
            y.append(coordinates["y"])

        connection_lines.append([x, y])

    # Plotting connections between stations
    for connection in connection_lines:
        plt.plot(connection[0], connection[1], c = '0.8')

    # plt.show()

def route_plot(traject):
    marked_cities = {}
    y_city = []
    x_city = []
    city_stations = stations_plot(stations)
    for cities in train_1:
        for city, coordinates in city_stations.items():
            if cities == city:
                marked_cities[cities] = coordinates

    for city_went, coordinates in marked_cities.items():
        # print(city_went, coordinates)
        y_city.append(coordinates["y"])
        x_city.append(coordinates["x"])

    plt.plot(x_city,y_city, '--b')
    plt.show()

stations = "StationsHolland_locaties.csv"
connections = "ConnectiesHolland.csv"

city_stations = stations_plot(stations)
# print(city_stations)
connection_plot(connections)

train_1 = ['Den Haag Centraal', 'Leiden Centraal', 'Alphen a/d Rijn', 'Gouda', 'Rotterdam Alexander', 'Gouda', 'Den Haag Centraal', 'Delft', 'Schiedam Centrum', 'Rotterdam Centraal']

route_plot(train_1)
