# Malve Rail Consulting
# 07/01/2025
#
# First version of the visualisation. Has to be put into functions and moved
# to train_table.py or helper_functions.py? Comments to be added.

import matplotlib.pyplot as plt
import csv

y = []
x = []
cities = {}

with open("StationsHolland_locaties.csv") as locaties_file:
    lines = locaties_file.readlines()[1:]
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        split_data = line.split(",")

        city = split_data[0]
        y_coordinate = float(split_data[1])
        x_coordinate = float(split_data[2])

        cities[city] = {"y":y_coordinate, "x":x_coordinate}

        # coordinates for scatter
        y.append(y_coordinate)
        x.append(x_coordinate)

# Plotting stations/cities
plt.scatter(x, y)

# Intialize connections dictionary
connections = {}

with open("ConnectiesHolland.csv") as connecties_file:
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
    plt.plot(connection[0], connection[1])

plt.show()
