
#from code.classes.train_table import Train_table
#from code.boxplot import create_box_plot
from code.classes.trajectanalyzer import TrajectAnalyzer
from code.classes.station import Station
from code.classes.experiment import Experiment
from code.classes.run_experiments import RunExperiments
from code.algorithms.depthfirst import DepthFirstCounter
from code.algorithms.randomise import Randomise
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
max_number_of_trajects = 10
max_time = 180
start_trajects = 9 # The minimum you need to visit all the connections in the Netherlands
end_trajects = 20 # The maximum of trajects if you use the Netherlands

if __name__ == "__main__":
    # ____Run single experiment____
    # e.g. with randomise and 2 trajects
    # randomised_experiment = Randomise(connections_file, locations_file, max_number_of_trajects, max_time)
    # randomised_experiment.run()
    # # Print output in terminal
    # randomised_experiment.print_output()
    # randomised_experiment.visualisation()

    # ____Run multiple experiments___
    # e.g. with randomise algorithms
    # temperature = 400
    # algorithm1 = Randomise
    # algorithm2 = SimulatedAnnealing
    #
    # number_of_experiments1 = 1000
    # number_of_experiments2 = 2000
    # r = RunExperiments(connections_file, locations_file, max_number_of_trajects, max_time,
    #                     number_of_experiments1, number_of_experiments2,
    #                     algorithm1_type = algorithm1,
    #                     algorithm2_type = algorithm2
    #                     )
    # r.run_first_algorithm()
    # r.save_all_objects("before")
    # r.run_second_algorithm(temperature)
    # r.save_all_objects("after")
    # r.print()
    # r.visualise()
    # r.to_csv()
    # traintable = r.best_yielding_experiment
    #r.create_boxplot()

      # # ____run DepthFirstCounter_____________
    # depth_first = DepthFirstCounter(connections_file, locations_file, max_number_of_trajects, max_time)
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
    # greedy_experiment = Greedy(connections_file, locations_file, max_number_of_trajects, max_time, use_randomise = False)
    # greedy_experiment.run()
    # greedy_experiment.print_output()
    # greedy_experiment.visualisation("greedy visualisation")

    #  __________GreedyLookahead___________
    # greedy_lookahead_experiment = GreedyLookahead(connections_file, locations_file, max_number_of_trajects, max_time, lookahead_depth= 2, use_randomise = False)
    # greedy_lookahead_experiment.run()
    # greedy_lookahead_experiment.print_output()

    # ____________Greedy________________________:
    # Note: The experiment for the greedy algoritm needs to run 1 time because it uses the heuristics of the
    # TrajectAnalyzer so every route will be the same.

    # algorithm1 = Greedy
    # algorithm2 = None
    # number_of_experiments1 = 1
    # r = RunExperiments(
    #     connections_file,
    #     locations_file,
    #     max_number_of_trajects,
    #     max_time,
    #     number_of_experiments1,
    #     number_of_experiments2 = None,
    #     algorithm1_type = algorithm1,
    #     algorithm2_type = algorithm2,
    #     start_trajects = start_trajects,
    #     end_trajects = end_trajects,
    #     lookahead_depth = None,
    #     use_randomise = False
    # )
    # r.run_first_algorithm()
    # r.save_all_collected_data("Greedy")
    # r.save_all_objects("Greedy", algorithm1)
    # r.box_plot("Greedy")

    #__________GreedyLookahead experiment: Heuristic of TrajectAnalyzer and Random____________________________
    # Note: We use a lookahead_depth from [2:6]. This is because a lookahead_depth of 1 is the same as a
    # greedy algoritm and a lookahead_depth of more than 6 will take too much memory to calculate so it will
    # take too long.
    # For the GreedyLookahead with the heuristic of the traject_analyzer we need to run the
    # algorithm only 1 time because every second iteration will be the same.

    # __________GreedyLookahead Heuristic of TrajectAnalyzer:
    # algorithm1 = GreedyLookahead
    # algorithm2 = None
    # number_of_experiments1 = 1
    # r = RunExperiments(
    #     connections_file,
    #     locations_file,
    #     max_number_of_trajects,
    #     max_time,
    #     number_of_experiments1,
    #     number_of_experiments2 = None,
    #     algorithm1_type = algorithm1,
    #     algorithm2_type = algorithm2,
    #     start_trajects = start_trajects,
    #     end_trajects = end_trajects,
    #     lookahead_depth = 2,
    #     use_randomise = False
    # )
    # r.run_first_algorithm()
    # r.save_all_collected_data("GreedyLookahead_TrajectAnalyzer_depht2")
    # r.save_all_objects("GreedyLookahead_TrajectAnalyzer_depth2", algorithm1)
    # r.box_plot("GreedyLookahead_TrajectAnalyzer_depth2")

    # __________GreedyLookahead Random:
    # algorithm1 = GreedyLookahead
    # algorithm2 = None
    # number_of_experiments1 = 100
    # r = RunExperiments(
    #     connections_file,
    #     locations_file,
    #     max_number_of_trajects,
    #     max_time,
    #     number_of_experiments1,
    #     number_of_experiments2 = None,
    #     algorithm1_type = algorithm1,
    #     algorithm2_type = algorithm2,
    #     start_trajects = start_trajects,
    #     end_trajects = end_trajects,
    #     lookahead_depth = 5,
    #     use_randomise = True
    # )
    # r.run_first_algorithm()
    # r.save_all_objects("GreedyLookahead_Random_dept5", algorithm1)
    # r.save_all_collected_data("GreedyLookahead_Random_depth5")
    # r.box_plot("GreedyLookahead_Random_depth5")
