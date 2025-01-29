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


def save_results(traintable, number_of_trajects, state_name, algorithm):
    """
    Saves the train table results as a CSV and PNG visualization.
    `state_name` indicates whether this is "before" or "after" the algorithm runs.
    """
    # get algorithm name as string
    algorithm_name = algorithm.__name__

    # Save CSV
    csv_filename = f"output/{number_of_trajects}_{algorithm_name}_{state_name}_results.csv"
    traintable.output_to_csv(csv_filename)

    # Save visualization
    visualization_filename = f"output/{number_of_trajects}_{algorithm_name}_{state_name}_visualization.png"
    traintable.visualisation(visualization_filename)

    print(f"Results saved: {csv_filename} and {visualization_filename}")
