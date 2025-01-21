# Baseline version

from code.classes.train_table import Train_table
from code.algorithms.randomise import random_start_station
from code.algorithms.randomise import random_select_next_station
from code.classes.trajectanalyzer import *
from code.boxplot import create_box_plot
from code.algorithms.depthfirst import DepthFirstCounter
from code.classes.station import Station


# Data files
locations_holland = "data/StationsHolland_locaties.csv"
connections_holland = "data/ConnectiesHolland.csv"
locations_national = "data/StationsNationaal_locaties.csv"
connections_national = "data/ConnectiesNationaal.csv"

# Parameters
connections = connections_holland
locations = locations_holland
number_of_trajects = 7
max_time = 120

if __name__ == "__main__":
    # Create baseline model
    baseline_train_table = Train_table(connections, locations, number_of_trajects, max_time, start_location_algorithm = random_start_station, select_next_station_algoritm = random_select_next_station)
    baseline_train_table.loop_for_solution()

    #Printing output in terminal
    baseline_train_table.print_output()

    #Creates csv output file and adds to output folder
    baseline_train_table.output_to_csv()

    #Creates visualisatin plot
    baseline_train_table.visualisation()

    #stations_dict = baseline_train_table.stations_dict
    #ta = TrajectAnalyzer(stations_dict) #, traject_histories)

    # #______TrajectAnalyzer tester______
    # stations_dict = baseline_train_table.stations_dict
    # ta = TrajectAnalyzer(stations_dict) #, traject_histories)
    # print(f"\n(Remaining) Dead ends: \n{ta.dead_ends}")
    # print(f"\n(Remaining) Odd connections: \n{ta.odd_connections}")
    # print(f"\n(Next) Start location: {ta.next_start_location}")
    #
    # #______TrajectAnalyzer tester______
    # depth_first = DepthFirstCounter(stations_dict, max_time)
    # # Count all possible trajectories for the map
    # total_possible_trajectories = depth_first.count_all_possible_trajectories()
    # print(f"Total possible trajectories for the map within {max_time} minutes: {total_possible_trajectories}")


    #______Box plot maker for random algorithm______
    #number_of_experiments = 100 # N
    #number_of_trajects = 7
    #plot_name = f"K Distributie Random Algoritme (N = {number_of_experiments})"

    #create_box_plot(connections, locations, number_of_trajects, max_time, start_location_algorithm = random_start_station, select_next_station_algoritm = random_select_next_station, N = number_of_experiments, plot_name = plot_name)
