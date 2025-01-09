# Malve Rail Consulting
# 07/01/2025
#
# Helper functions to import and clean files, turn cleaned up files into dicts.

import csv

def file_import(file):
    """ Imports file and cleans it up. Returns it as list of lists.
    """
    clean_file = []

    with open(file) as f:
        lines = f.readlines()[1:]
        for line in lines:
            line = line.strip()
            if line == "":
                continue
            split_data = line.split(",")

            clean_file.append(split_data)

    return clean_file

def connections_dict(connections):
    connections_dict = {}
    clean_connections = file_import(connections)

    for connection in clean_connections:
        station1, station2, time = connection
        connections_dict[station1+"_"+station2] = time

    return connections_dict

def connecting_options_dict(connections):
    # connections_options_dict
    connecting_options = {}
    clean_connections = file_import(connections)

    for connection in clean_connections:
        station1, station2, time = connection

        # Add stations to dictionary if not already present
        if station1 not in connecting_options:
            connecting_options[station1] = {}
        if station2 not in connecting_options:
            connecting_options[station2] = {}

        # Add connecting city and time to dictionary
        connecting_options[station1][station1+"_"+station2] = time
        connecting_options[station2][station1+"_"+station2] = time

    return connecting_options



def locations_dict(locations):
    """ Creates dictionary with locations of stations.

    To do: add failsafe for when input file is not of right dimensions
    """
    locations_dict = {}
    clean_locations = file_import(locations)

    for location in clean_locations:
        station, x, y = location

        locations_dict[station] = [x, y]


    return locations_dict


def connections_dict_old(connections):
    # connections_options_dict
    """ Creates nested dictionary with stations and connecting stations with
    the time it takes to get there in minutes.

    Note: old code, probably not useful anymore
    """
    connections_dict = {}
    clean_connections = file_import(connections)

    for connection in clean_connections:
        station1, station2, time = connection

        # Add stations to dictionary if not already present
        if station1 not in connections_dict:
            connections_dict[station1] = {}
        if station2 not in connections_dict:
            connections_dict[station2] = {}

        # Add connecting city and time to dictionary
        connections_dict[station1][station2] = time
        connections_dict[station2][station1] = time

    return connections_dict

# debugging
#connections = "ConnectiesHolland.csv"
#test = connecting_options_dict(connections)
#print(test)
