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
