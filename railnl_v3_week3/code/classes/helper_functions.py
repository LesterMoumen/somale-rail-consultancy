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

def sorted_connection(station1, station2, separator="_"):
    """ Returns input two stations as sorted connection string.
    e.g. "Den Helder" and "Alkmaar" become "Alkmaar_Den Helder"
    """
    sorted_connection = sorted([station1, station2])

    connection_str = f"{sorted_connection[0]}_{sorted_connection[1]}"

    return connection_str
