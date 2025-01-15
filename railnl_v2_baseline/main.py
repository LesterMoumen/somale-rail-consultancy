from code.classes.train_table import Train_table

# Input files
locations = "data/StationsHolland_locaties.csv"
connections = "data/ConnectiesHolland.csv"
#locations = "StationsNationaal_locaties.csv"
#connections = "ConnectiesNationaal.csv"

if __name__ == "__main__":
    # Create baseline model with 7 locations and 120 minutes max
    baseline_train_table = Train_table(connections, locations, 7, max_time = 120)
    baseline_train_table.create_table()

    # Printing output in terminal for debugging purposes
    baseline_train_table.print_output()

    # Creates csv output file and adds to output folder
    baseline_train_table.output_to_csv()

    # Note: buggy! Will not work
    baseline_train_table.visualisation()
