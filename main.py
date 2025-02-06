
from code.classes.trajectanalyzer import TrajectAnalyzer
from code.algorithms.depthfirst import DepthFirstCounter
from code.classes.station import Station
from code.classes.experiment import Experiment
from code.algorithms.randomise import Randomise
from code.classes.run_experiments import RunExperiments
from code.algorithms.greedy import Greedy
from code.algorithms.greedy import GreedyLookahead
from code.algorithms.hillclimber import HillClimber
from code.algorithms.simulatedannealing import SimulatedAnnealing
from code.classes.main_interface import select_first_algorithm, select_second_algorithm, get_algorithm_parameters
import itertools

# Data files
locations_holland = "data/StationsHolland_locaties.csv"
connections_holland = "data/ConnectiesHolland.csv"
locations_national = "data/StationsNationaal_locaties.csv"
connections_national = "data/ConnectiesNationaal.csv"

# Parameters
locations_file = locations_national
connections_file = connections_national
max_trajects = 20
max_time = 180



if __name__ == "__main__":
    # #____Select your own experiment___
    # algorithm1 = select_first_algorithm()
    # if algorithm1 is not None:
    #     parameters1 = get_algorithm_parameters(algorithm1) # 'num_experiments1', 'use_randomise', 'depth'
    #
    # algorithm2 = select_second_algorithm()
    # if algorithm2 is not None:
    #     parameters2 = get_algorithm_parameters(algorithm2) # 'num_experiments2', 'temperature', 'alpha', 'num_tracks', 'num_trajects'
    #
    # # If both algorithms are None, exit the program
    # if algorithm1 is None and algorithm2 is None:
    #     print("No algorithms selected. Exiting.")
    #     exit()
    #
    # # Also exits if first algorithm is None and second is given -> Hc and Sa require traintable
    # if algorithm1 is None and algorithm2 is not None:
    #     print("Can't optimalize through iterative model without a traintable.")
    #     exit()
    #
    # if algorithm1 is not None and algorithm2 is None:
    #     parameters2 = {'number_of_experiments2': 0}
    #
    # # Initialize and run the experiments
    # r = RunExperiments(connections_file, locations_file, max_trajects, max_time,
    #                    parameters1.get('number_of_experiments1', 1000), parameters2.get('number_of_experiments2', 1000),
    #                    algorithm1_type=algorithm1, algorithm2_type=algorithm2)
    #
    #
    # if algorithm1 is not None:
    #     if algorithm1 in [Randomise, GreedyLookahead, Greedy]:
    #         r.run_constructive_algorithm(**parameters1)
    #
    #     #r.run_first_algorithm()
    #     r.save_all_objects(algorithm1, r.experiment_object_dict)
    #     r.save_all_collected_data(filename=algorithm1.__name__)
    #
    #
    # if algorithm2 is not None:
    #     if algorithm2 == SimulatedAnnealing:
    #         r.run_iterative_algorithm(**parameters2)
    #     else: # HillClimber
    #         r.run_iterative_algorithm(**parameters2)
    #
    #     r.save_all_objects(algorithm2, r.experiment_object_dict2)




    #____Run with multiple parameters___
    parameters1 = {
    'depth': 3,
    'use_randomise': True
    }

    parameters2 = {
        'temperature': [10, 100, 500, 1000],
        'alpha': [0.85, 0.95, 0.99, 0.998],
        'mutate_trajects_number': [1, 2, 3],
        'mutate_tracks_number': [1, 2, 3, 4, 5]
    }

    algorithm1 = Randomise
    algorithm2 = HillClimber

    number_of_experiments1 = 1000
    number_of_experiments2 = 30000

    r = RunExperiments(connections_file, locations_file, max_trajects, max_time,
                       number_of_experiments1, number_of_experiments2,
                       algorithm1_type=algorithm1,
                       algorithm2_type=algorithm2)

    r.run_constructive_algorithm()
    r.save_all_objects(algorithm1.__name__, r.experiment_object_dict)
    r.save_all_collected_data(filename=algorithm1.__name__)

    for traject_number in parameters2['mutate_trajects_number']:
        for track_number in parameters2['mutate_tracks_number']:
            # Create a new dictionary with the correct parameteres for HillCLimber
            parameters = {'mutate_trajects_number': traject_number, 'mutate_tracks_number': track_number}

            # Check if HillClimber, else skip
            if algorithm2 == HillClimber:
                r.run_iterative_algorithm(**parameters)
                # Create a filename for this iteration
                filename = f"{traject_number}_{track_number}_{algorithm2.__name__}"
                # Save the results with the updated filename
                r.save_all_objects(filename, r.experiment_object_dict2)


            for alpha in parameters2['alpha']:
                for temperature in parameters2['temperature']:
                    # Create a new dictionary with the correct parameteres for Simulated Annealing
                    second_parameters = {**parameters, 'temperature': temperature, 'alpha': alpha}

                    r.run_iterative_algorithm(**second_parameters)
                    # Create a new filename for this iteration
                    second_filename = f"{traject_number}_{track_number}_{alpha}_{temperature}_{algorithm2.__name__}"
                    # Save the results with the updated filename
                    r.save_all_objects(second_filename, r.experiment_object_dict2)


    # ____run DepthFirstCounter_____________

    # depth_first = DepthFirstCounter(connections_file, locations_file, 1, 180)
    # total_possible_trajectories = depth_first.count_all_possible_trajectories()
    # print(f"Total possible trajectories for the map within {max_time} minutes: {total_possible_trajectories}")
