import csv

def file_import(file):
    """ Imports file and cleans it up. Returns it as list of lists.
    """
    clean_file = []

    with open(file) as f:
        lines = f.readlines()[1:]
        for line in lines:
            line = line.strip()
            if line == "":
                continue
            split_data = line.split(",")

            clean_file.append(split_data)

    return clean_file

def sorted_connection(station1, station2, separator="_"):
    """ Returns input two stations as sorted connection string.
    e.g. "Den Helder" and "Alkmaar" become "Alkmaar_Den Helder"
    """
    sorted_connection = sorted([station1, station2])

    connection_str = f"{sorted_connection[0]}_{sorted_connection[1]}"

    return connection_str


def save_results(traintable, number_of_trajects, algorithm):
    """
    Saves the train table results as a CSV and PNG visualization.
    `state_name` indicates whether this is "before" or "after" the algorithm runs.
    """
    # get algorithm name as string
    algorithm_name = algorithm.__name__

    # Save CSV
    csv_filename = f"output/{number_of_trajects}_{algorithm_name}_results.csv"
    traintable.output_to_csv(csv_filename)

    # Save visualization
    visualization_filename = f"output/{number_of_trajects}_{algorithm_name}_visualization.png"
    traintable.visualisation(visualization_filename)

    print(f"Results saved: {csv_filename} and {visualization_filename}")

#
# def select_first_algorithm():
#     print(f"Select the algorithm for the first algorithm:")
#     print("1. Randomise")
#     print("2. Greedy")
#     print("3. GreedyLookahead")
#     print("4. None (do not use an algorithm)")
#
#     choice = input(f"Enter the number corresponding with one of the algorithms (1-4): ")
#
#     if choice == '1':
#         return Randomise
#     elif choice == '2':
#         return Greedy
#     elif choice == '3':
#         return GreedyLookahead
#     elif choice == '4':
#         return None
#     else:
#         print("Invalid choice, please choose a number between 1 and 4.")
#         return select_first_algorithm()
#
# def select_second_algorithm():
#     print(f"Select the algorithm for second algorithm:")
#     print("1. HillClimber")
#     print("2. SimulatedAnnealing")
#     print("3. None (do not use an algorithm)")
#
#     choice = input(f"Enter the number corresponding with one of the algorithms (1-3): ")
#
#     if choice == '1':
#         return HillClimber
#     elif choice == '2':
#         return SimulatedAnnealing
#     elif choice == '3':
#         return None
#     else:
#         print("Invalid choice, please choose a number between 1 and 3.")
#         return select_second_algorithm()
#
# def get_algorithm_parameters(algorithm):
#
#     if not isinstance(algorithm, str):
#         algorithm = algorithm.__name__
#
#     if algorithm == 'Randomise' or algorithm == 'Greedy':
#         num_experiments = int(input(f"Enter the number of experiments for {algorithm}: "))
#         return {'number_of_experiments1': num_experiments}
#
#     elif algorithm == 'Greedy':
#         num_experiments = int(input(f"Enter the number of experiments for {algorithm}: "))
#         response = input("Do you want to use Randomise with the algorithm? Enter 'yes' or 'no': ").lower()
#         if response == 'yes':
#             use_randomise = True
#         elif response == 'no':
#             use_randomise = False
#         else:
#             print("Invalid input. Please enter 'yes' or 'no'.")
#
#         return {'number_of_experiments1': num_experiments, 'depth': depth, 'use_randomise': use_randomise}
#
#     elif algorithm == 'GreedyLookahead':
#         num_experiments = int(input(f"Enter the number of experiments for {algorithm}: "))
#         depth = int(input("Enter the depth for GreedyLookahead: "))
#         response = input("Do you want to use Randomise with the algorithm? Enter 'yes' or 'no': ").lower()
#         if response == 'yes':
#             use_randomise = True
#         elif response == 'no':
#             use_randomise = False
#         else:
#             print("Invalid input. Please enter 'yes' or 'no'.")
#
#         return {'number_of_experiments1': num_experiments, 'depth': depth, 'use_randomise': use_randomise}
#
#     elif algorithm == 'HillClimber':
#         num_experiments = int(input(f"Enter the number of experiments for {algorithm}: "))
#         num_tracks = int(input("Enter the number of tracks you want to mutate for HillClimber: "))
#         num_trajects = int(input("Enter the number of trajects you want to mutate for HillClimber: "))
#         return {'number_of_experiments2': num_experiments, 'mutate_tracks_number': num_tracks, 'mutate_trajects_number': num_trajects}
#
#     elif algorithm == 'SimulatedAnnealing':
#         num_experiments = int(input(f"Enter the number of experiments for {algorithm}: "))
#         num_tracks = int(input("Enter the number of tracks you want to mutate for HillClimber: "))
#         num_trajects = int(input("Enter the number of trajects you want to mutate for HillClimber: "))
#         temperature = int(input("Enter the temperature for SimulatedAnnealing: "))
#         alpha = float(input("Enter the alpha for SimulatedAnnealing (0 to 1): "))
#         return {'number_of_experiments2': num_experiments, 'temperature': temperature, 'alpha': alpha,
#             'mutate_tracks_number': num_tracks, 'mutate_trajects_number': num_trajects}
#
#     return {}
