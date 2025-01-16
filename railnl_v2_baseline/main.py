# Baseline version

from code.classes.train_table import Train_table

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
    baseline_train_table = Train_table(connections, locations, number_of_trajects, max_time)
    baseline_train_table.create_table()

    # Printing output in terminal
    #baseline_train_table.print_output()

    # Creates csv output file and adds to output folder
    baseline_train_table.output_to_csv()

    # Creates visualisatin plot
    baseline_train_table.visualisation()
