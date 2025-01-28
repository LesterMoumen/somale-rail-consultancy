# Baseline version

#from code.classes.train_table import Train_table
from code.classes.trajectanalyzer import TrajectAnalyzer
#from code.boxplot import create_box_plot
from code.algorithms.depthfirst import DepthFirstCounter
from code.classes.station import Station
from code.algorithms.experiment import Experiment
from code.algorithms.randomise import Randomise
from code.algorithms.run_experiments import RunExperiments
from code.algorithms.greedy import Greedy
from code.algorithms.greedy import GreedyLookahead
from code.algorithms.hillclimber import HillClimber
from code.algorithms.simulatedannealing import SimulatedAnnealing


# Data files
locations_holland = "data/StationsHolland_locaties.csv"
connections_holland = "data/ConnectiesHolland.csv"
locations_national = "data/StationsNationaal_locaties.csv"
connections_national = "data/ConnectiesNationaal.csv"

# Parameters
connections_file = connections_national
locations_file = locations_national
max_number_of_trajects = 20
max_time = 180

if __name__ == "__main__":
    # ____Run single experiment____
    # e.g. with randomise and 2 trajects
    number_of_trajects = 1
    # randomised_experiment = Randomise(connections_file, locations_file, number_of_trajects, max_time)
    # randomised_experiment.run()
    # # Print output in terminal
    # randomised_experiment.print_output()
    # randomised_experiment.visualisation()
    #
    # # Test trajectanalyzer
    # stations_dict = randomised_experiment.stations_dict
    # connections_dict = randomised_experiment.connections_dict
    # traject_list = randomised_experiment.traject_list
    # connections_set = randomised_experiment.connections_set
    #
    # ta = TrajectAnalyzer(stations_dict, connections_dict, traject_list, connections_set)
    #
    # dead_ends = ta.dead_ends
    # odd_connections = ta.odd_connections
    # next_start_station = ta.find_next_start_location()
    # print("Dead ends", dead_ends)
    # print("Odd connection", odd_connections)
    # print("Next start location:", next_start_station)

    # ____Run multiple experiments___
    # e.g. with randomise algorithms
    temperature = 400
    algorithm1 = Randomise
    algorithm2 = SimulatedAnnealing



    number_of_experiments1 = 1000
    number_of_experiments2 = 2000
    r = RunExperiments(connections_file, locations_file, max_number_of_trajects, max_time,
                        number_of_experiments1, number_of_experiments2,
                        algorithm1_type = algorithm1,
                        algorithm2_type = algorithm2
                        )
    r.run_first_algorithm()
    r.save_all_objects("before")
    r.run_second_algorithm(temperature)
    r.save_all_objects("after")
    # r.print()
    # r.visualise()
    # r.to_csv()
    # traintable = r.best_yielding_experiment
    #r.create_boxplot()

      # # ____run DepthFirstCounter_____________
    # depth_first = DepthFirstCounter(connections_file, locations_file, number_of_trajects, max_time)
    # total_possible_trajectories = depth_first.count_all_possible_trajectories()
    # print(f"Total possible trajectories for the map within {max_time} minutes: {total_possible_trajectories}")

    #____run HillClimber_____________
    # randomised_experiment = Randomise(connections_file, locations_file, max_number_of_trajects, max_time)
    # traintable = randomised_experiment.run_till_solution()
    #
    # hill_climber = HillClimber(traintable)
    # hill_climber.run(1000, verbose=True)

    # traintable.print_output()
    # traintable.visualisation()

    # ____________Greedy____________
    greedy_experiment = Greedy(connections_file, locations_file, number_of_trajects, max_time)
    # greedy_experiment.run()
    # greedy_experiment.print_output()
    # greedy_experiment.visualisation("greedy")
    # greedy_experiment.output_to_csv("Greedy csv ")
    # # __________GreedyLookahead___________
<<<<<<< HEAD
    greedy_lookahead_experiment = GreedyLookahead(connections_file, locations_file, number_of_trajects, max_time, use_randomise = False)
    # greedy_lookahead_experiment.run_till_solution()
    greedy_lookahead_experiment.run()
    greedy_lookahead_experiment.print_output()
=======
    # greedy_lookahead_experiment = GreedyLookahead(connections_file, locations_file, number_of_trajects, max_time)
    # greedy_lookahead_experiment.run()
    # greedy_lookahead_experiment.print_output()
>>>>>>> 980cff64847d798515e9ebc80ca5748e5b637edb
    # greedy_lookahead_experiment.visualisation("GreedyLookahead")
    # greedy_lookahead_experiment.output_to_csv("GreedyLookahead csv")

    # __________GreedyLookahead___________ experiment:
    # algorithm = Greedy
    # number_of_experiments = 50
    # r = RunExperiments(connections_file, locations_file, max_number_of_trajects, max_time, number_of_experiments, algorithm_type = algorithm)
    # # r.run()
    # # r.create_boxplot()
    #
    # # __________GreedyLookahead___________ experiment:
    # algorithm = GreedyLookahead
    # number_of_experiments = 50
    # r = RunExperiments(connections_file, locations_file, max_number_of_trajects, max_time, number_of_experiments, algorithm_type = algorithm)
    # # r.run()
    # # r.create_boxplot()
