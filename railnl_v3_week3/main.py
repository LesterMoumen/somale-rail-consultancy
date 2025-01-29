
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
    greedy_lookahead_experiment = GreedyLookahead(connections_file, locations_file, max_number_of_trajects, max_time, use_randomise = False)
    # greedy_lookahead_experiment.run()
    # greedy_lookahead_experiment.print_output()


    #__________GreedyLookahead random experiment___________
    algorithm1 = GreedyLookahead
    algorithm2 = None
    number_of_experiments1 = 2
    r = RunExperiments(connections_file, locations_file, max_number_of_trajects, max_time,
                        number_of_experiments1, number_of_experiments2 = None, algorithm1_type = algorithm1, algorithm2_type = algorithm2, use_randomise = True)
    r.run_first_algorithm()
    r.save_all_collected_data("Greed")
    # r.save_all_objects("GreedyLookahead random", algorithm1)
    # r.print()
    # r.visualise_experiment("greedy_look")
    # r.to_csv()
    # r.box_plot("GreedyLookahead random")

    # __________ GreedyLookahead TrajectAnalyzer experiment_________
    algorithm1 = GreedyLookahead
    algorithm2 = None
    number_of_experiments1 = 2
    start_trajects = 7
    end_trajects = 17
    r = RunExperiments(connections_file, locations_file, max_number_of_trajects, max_time,
                        number_of_experiments1, number_of_experiments2 = None, algorithm1_type = algorithm1, algorithm2_type = algorithm2, use_randomise = False)
    # r.run_first_algorithm()
    # r.save_all_objects("GreedyLookahead TrajectAnalyzer", algorithm1)
    # r.box_plot("GreedyLookahead TrajectAnalyzer")
