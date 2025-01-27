# Baseline version

#from code.classes.train_table import Train_table
from code.classes.trajectanalyzer import TrajectAnalyzer
#from code.boxplot import create_box_plot
#from code.algorithms.depthfirst import DepthFirstCounter
#from code.classes.station import Station
from code.algorithms.experiment import Experiment
from code.algorithms.randomise import Randomise
from code.algorithms.run_experiments import RunExperiments
from code.algorithms.greedy import Greedy
from code.algorithms.greedy import GreedyLookahead


# Data files
locations_holland = "data/StationsHolland_locaties.csv"
connections_holland = "data/ConnectiesHolland.csv"
locations_national = "data/StationsNationaal_locaties.csv"
connections_national = "data/ConnectiesNationaal.csv"

# Parameters
connections_file = connections_holland
locations_file = locations_holland
max_number_of_trajects = 7
max_time = 120

if __name__ == "__main__":
    # ____Run single experiment____
    # e.g. with randomise and 2 trajects
    number_of_trajects = 1
    randomised_experiment = Randomise(connections_file, locations_file, number_of_trajects, max_time)
    randomised_experiment.run()
    # Print output in terminal
    randomised_experiment.print_output()
    # randomised_experiment.visualisation()

    # Test trajectanalyzer
    stations_dict = randomised_experiment.stations_dict
    connections_dict = randomised_experiment.connections_dict
    traject_list = randomised_experiment.traject_list
    connections_set = randomised_experiment.connections_set

    ta = TrajectAnalyzer(stations_dict, connections_dict, traject_list, connections_set)

    dead_ends = ta.dead_ends
    odd_connections = ta.odd_connections
    next_start_station = ta.find_next_start_location()
    print("Dead ends", dead_ends)
    print("Odd connection", odd_connections)
    print("Next start location:", next_start_station)

    # ____Run multiple experiments___
    # e.g. with randomise algorithms
    #algorithm = Randomise
    #number_of_experiments = 100
    #r = RunExperiments(connections_file, locations_file, max_number_of_trajects, max_time, number_of_experiments, algorithm_type = algorithm)
    #r.run()
    #r.create_boxplot()


    # ____________Greedy____________
    greedy_experiment = Greedy(connections_file, locations_file, number_of_trajects, max_time)
    greedy_experiment.run()
    greedy_experiment.print_output()
    # greedy_experiment.visualisation()
    # __________GreedyLookahead___________
    greedy_lookahead_experiment = GreedyLookahead(connections_file, locations_file, number_of_trajects, max_time)
    greedy_lookahead_experiment.run()
    greedy_lookahead_experiment.print_output()
    # greedy_lookahead_experiment.visualisation()

    # __________GreedyLookahead___________ experiment:
    algorithm = Greedy
    number_of_experiments = 50
    r = RunExperiments(connections_file, locations_file, max_number_of_trajects, max_time, number_of_experiments, algorithm_type = algorithm)
    # r.run()
    # r.create_boxplot()

    # __________GreedyLookahead___________ experiment:
    algorithm = GreedyLookahead
    number_of_experiments = 50
    r = RunExperiments(connections_file, locations_file, max_number_of_trajects, max_time, number_of_experiments, algorithm_type = algorithm)
    # r.run()
    # r.create_boxplot()
