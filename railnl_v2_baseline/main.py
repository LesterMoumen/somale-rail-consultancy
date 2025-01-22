# Baseline version

from code.classes.train_table import Train_table
from code.algorithms.randomise import random_start_station
from code.algorithms.randomise import random_select_next_station
# from code.algortihms.greedy import greedy as gr

# Data files
locations_holland = "data/StationsHolland_locaties.csv"
connections_holland = "data/ConnectiesHolland.csv"
locations_national = "data/StationsNationaal_locaties.csv"
connections_national = "data/ConnectiesNationaal.csv"

# Parameters
connections = connections_holland
locations = locations_holland
number_of_trajects = 4
max_time = 120

if __name__ == "__main__":
    # Create baseline model
    baseline_train_table = Train_table(connections, locations, number_of_trajects, max_time, start_location_algorithm = random_start_station, select_next_station_algoritm = random_select_next_station)
    baseline_train_table.create_table()

    # Printing output in terminal
    #baseline_train_table.print_output()

    # Creates csv output file and adds to output folder
    baseline_train_table.output_to_csv()

    # Creates visualisatin plot
    baseline_train_table.visualisation()
    # -------------Greedy ----------------------------
    # greedy = gr.Greedy(baseline_train_table())
    # greedy.run()
