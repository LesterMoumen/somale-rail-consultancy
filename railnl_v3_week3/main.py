
#from code.classes.train_table import Train_table
from code.classes.trajectanalyzer import TrajectAnalyzer
#from code.boxplot import create_box_plot
from code.algorithms.depthfirst import DepthFirstCounter
from code.classes.station import Station
from code.classes.experiment import Experiment
from code.algorithms.randomise import Randomise
from code.classes.run_experiments import RunExperiments
from code.algorithms.greedy import Greedy
from code.algorithms.greedy import GreedyLookahead
from code.algorithms.hillclimber import HillClimber
from code.algorithms.simulatedannealing import SimulatedAnnealing
#from code.classes.helper_functions import select_first_algorithm, select_second_algorithm, get_algorithm_parameters

# Data files
locations_holland = "data/StationsHolland_locaties.csv"
connections_holland = "data/ConnectiesHolland.csv"
locations_national = "data/StationsNationaal_locaties.csv"
connections_national = "data/ConnectiesNationaal.csv"

# Parameters
connections_file = connections_national
locations_file = locations_national
max_trajects = 3
max_time = 180


def select_first_algorithm():
    print(f"Select the algorithm for the first algorithm:")
    print("1. Randomise")
    print("2. Greedy")
    print("3. GreedyLookahead")
    print("4. None (do not use an algorithm)")

    choice = input(f"Enter the number corresponding with one of the algorithms (1-4): ")

    if choice == '1':
        return Randomise
    elif choice == '2':
        return Greedy
    elif choice == '3':
        return GreedyLookahead
    elif choice == '4':
        return None
    else:
        print("Invalid choice, please choose a number between 1 and 4.")
        return select_first_algorithm()

def select_second_algorithm():
    print(f"Select the algorithm for second algorithm:")
    print("1. HillClimber")
    print("2. SimulatedAnnealing")
    print("3. None (do not use an algorithm)")

    choice = input(f"Enter the number corresponding with one of the algorithms (1-3): ")

    if choice == '1':
        return HillClimber
    elif choice == '2':
        return SimulatedAnnealing
    elif choice == '3':
        return None
    else:
        print("Invalid choice, please choose a number between 1 and 3.")
        return select_second_algorithm()

def get_algorithm_parameters(algorithm):

    if not isinstance(algorithm, str):
        algorithm = algorithm.__name__

    if algorithm == 'Randomise' or algorithm == 'Greedy':
        num_experiments = int(input(f"Enter the number of experiments for {algorithm}: "))
        return {'number_of_experiments1': num_experiments}

    elif algorithm == 'Greedy':
        num_experiments = int(input(f"Enter the number of experiments for {algorithm}: "))
        response = input("Do you want to use Randomise with the algorithm? Enter 'yes' or 'no': ").lower()
        if response == 'yes':
            use_randomise = True
        elif response == 'no':
            use_randomise = False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

        return {'number_of_experiments1': num_experiments, 'depth': depth, 'use_randomise': use_randomise}

    elif algorithm == 'GreedyLookahead':
        num_experiments = int(input(f"Enter the number of experiments for {algorithm}: "))
        depth = int(input("Enter the depth for GreedyLookahead: "))
        response = input("Do you want to use Randomise with the algorithm? Enter 'yes' or 'no': ").lower()
        if response == 'yes':
            use_randomise = True
        elif response == 'no':
            use_randomise = False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

        return {'number_of_experiments1': num_experiments, 'depth': depth, 'use_randomise': use_randomise}

    elif algorithm == 'HillClimber':
        num_experiments = int(input(f"Enter the number of experiments for {algorithm}: "))
        num_tracks = int(input("Enter the number of tracks you want to mutate for HillClimber: "))
        num_trajects = int(input("Enter the number of trajects you want to mutate for HillClimber: "))
        return {'number_of_experiments2': num_experiments, 'mutate_tracks_number': num_tracks, 'mutate_trajects_number': num_trajects}

    elif algorithm == 'SimulatedAnnealing':
        num_experiments = int(input(f"Enter the number of experiments for {algorithm}: "))
        num_tracks = int(input("Enter the number of tracks you want to mutate for HillClimber: "))
        num_trajects = int(input("Enter the number of trajects you want to mutate for HillClimber: "))
        temperature = int(input("Enter the temperature for SimulatedAnnealing: "))
        alpha = float(input("Enter the alpha for SimulatedAnnealing (0 to 1): "))
        return {'number_of_experiments2': num_experiments, 'temperature': temperature, 'alpha': alpha,
            'mutate_tracks_number': num_tracks, 'mutate_trajects_number': num_trajects}

    return {}

if __name__ == "__main__":
    # Get algorithm selection
    algorithm1 = select_first_algorithm()
    if algorithm1 is not None:
        parameters1 = get_algorithm_parameters(algorithm1) # 'num_experiments1', 'use_randomise', 'depth'

    algorithm2 = select_second_algorithm()
    if algorithm2 is not None:
        parameters2 = get_algorithm_parameters(algorithm2) # 'num_experiments2', 'temperature', 'alpha', 'num_tracks', 'num_trajects'

    # If both algorithms are None, exit the program
    if algorithm1 is None and algorithm2 is None:
        print("No algorithms selected. Exiting.")
        exit()

    # Also exits if first algorithm is None and second is given -> Hc and Sa require traintable
    if algorithm1 is None and algorithm2 is not None:
        print("Can't optimalize through iterative model without a traintable.")
        exit()

    if algorithm1 is not None and algorithm2 is None:
        parameters2 = {'number_of_experiments2': 0}

    # Initialize and run the experiments
    r = RunExperiments(connections_file, locations_file, max_trajects, max_time,
                       parameters1.get('number_of_experiments1', 1000), parameters2.get('number_of_experiments2', 1000),
                       algorithm1_type=algorithm1, algorithm2_type=algorithm2)


    if algorithm1 is not None:
        if algorithm1 in [Randomise, GreedyLookahead, Greedy]:
            r.run_constructive_algorithm(**parameters1)

        #r.run_first_algorithm()
        r.save_all_objects(algorithm1, r.experiment_object_dict)
        r.save_all_collected_data(filename=algorithm1.__name__)


    if algorithm2 is not None:
        if algorithm2 == SimulatedAnnealing:
            r.run_iterative_algorithm(**parameters2)
        else: # HillClimber
            r.run_iterative_algorithm(**parameters2)

        r.save_all_objects(algorithm2, r.experiment_object_dict2)




# if __name__ == "__main__":
#     # ____Run single experiment____
#     # e.g. with randomise and 2 trajects
#     # randomised_experiment = Randomise(connections_file, locations_file, max_number_of_trajects, max_time)
#     # randomised_experiment.run()
#     # # Print output in terminal
#     # randomised_experiment.print_output()
#     # randomised_experiment.visualisation()
#
#     # ____Run multiple experiments___
#     # e.g. with randomise algorithms
#     # temperature = 400
#     # algorithm1 = Randomise
#     # algorithm2 = SimulatedAnnealing
#     #
#     # number_of_experiments1 = 1000
#     # number_of_experiments2 = 2000
#     # r = RunExperiments(connections_file, locations_file, max_number_of_trajects, max_time,
#     #                     number_of_experiments1, number_of_experiments2,
#     #                     algorithm1_type = algorithm1,
#     #                     algorithm2_type = algorithm2
#     #                     )
#     # r.run_first_algorithm()
#     # r.save_all_objects("before")
#     # r.run_second_algorithm(temperature)
#     # r.save_all_objects("after")
#     # r.print()
#     # r.visualise()
#     # r.to_csv()
#     # traintable = r.best_yielding_experiment
#     #r.create_boxplot()
#
#       # # ____run DepthFirstCounter_____________
#     # depth_first = DepthFirstCounter(connections_file, locations_file, max_number_of_trajects, max_time)
#     # total_possible_trajectories = depth_first.count_all_possible_trajectories()
#     # print(f"Total possible trajectories for the map within {max_time} minutes: {total_possible_trajectories}")
#
#     #____run HillClimber_____________
#     # randomised_experiment = Randomise(connections_file, locations_file, max_number_of_trajects, max_time)
#     # traintable = randomised_experiment.run_till_solution()
#     #
#     # hill_climber = HillClimber(traintable)
#     # hill_climber.run(1000, verbose=True)
#
#     # traintable.print_output()
#     # traintable.visualisation()
#
#     # ____________Greedy____________
#     # greedy_experiment = Greedy(connections_file, locations_file, max_number_of_trajects, max_time, use_randomise = False)
#     # greedy_experiment.run()
#     # greedy_experiment.print_output()
#     # greedy_experiment.visualisation("greedy visualisation")
#
#     #  __________GreedyLookahead___________
#     #greedy_lookahead_experiment = GreedyLookahead(connections_file, locations_file, max_number_of_trajects, max_time, use_randomise = False)
#     # greedy_lookahead_experiment.run()
#     # greedy_lookahead_experiment.print_output()
#
#
#     #__________GreedyLookahead random experiment___________
#     algorithm1 = Randomise, Greedy
#     number_of_experiments1 = 1000
#     if:
#     algorithm2 = HillClimber
#
#     if algoritme = Simulated
#     number_of_experiments2 = 3000
#     temperature = 1000
#     r = RunExperiments(connections_file, locations_file, max_number_of_trajects, max_time,
#                         number_of_experiments1, number_of_experiments2, algorithm1_type = algorithm1, algorithm2_type = algorithm2, use_randomise = True)
#     r.run_first_algorithm()
#     r.save_all_objects(algorithm1)
#     r.run_second_algorithm(temperature)
#     r.save_all_objects(algorithm2)
#     # r.print()
#     # r.visualise_experiment("greedy_look")
#     #r.save_all_collected_data("Greed_RNDM")
#     # r.to_csv()
#     # r.box_plot("GreedyLookahead random")
#
#     # __________ GreedyLookahead TrajectAnalyzer experiment_________
#     # algorithm1 = GreedyLookahead
#     # algorithm2 = None
#     # number_of_experiments1 = 2
#     # start_trajects = 9
#     # end_trajects = 17
#     # r = RunExperiments(connections_file, locations_file, max_number_of_trajects, max_time,
#     #                     number_of_experiments1, number_of_experiments2 = None, algorithm1_type = algorithm1, algorithm2_type = algorithm2, use_randomise = False)
#     # r.run_first_algorithm()
#     # r.save_all_collected_data("Greed_TA")
#     # r.run_first_algorithm()
#     # r.save_all_objects("GreedyLookahead TrajectAnalyzer", algorithm1)
#     # r.box_plot("GreedyLookahead TrajectAnalyzer")
