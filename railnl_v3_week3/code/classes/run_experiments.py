import csv
import matplotlib.pyplot as plt
from code.classes.experiment import Experiment
from code.classes.visualisation import Visualisation
from code.algorithms.randomise import Randomise
from code.classes.helper_functions import save_results
from code.algorithms.hillclimber import HillClimber
from code.algorithms.simulatedannealing import SimulatedAnnealing
from code.algorithms.greedy import Greedy
from code.algorithms.greedy import GreedyLookahead
import copy


class RunExperiments():
    def __init__(self, connections_file, locations_file, max_number_of_trajects, max_time,
                 number_of_experiments1, number_of_experiments2, algorithm1_type,
                 algorithm2_type, start_trajects=9, end_trajects=12, use_randomise=False):
        self.connections_file = connections_file
        self.locations_file = locations_file
        self.max_number_of_trajects = max_number_of_trajects
        self.max_time = max_time
        self.number_of_experiments1 = number_of_experiments1
        self.number_of_experiments2 = number_of_experiments2
        self.algorithm1 = algorithm1_type
        self.algorithm2 = algorithm2_type
        self.use_randomise = use_randomise
        self.start_trajects = start_trajects
        self.end_trajects = end_trajects

        self.experiment_object_dict = {}  # Stores the best experiment objects for each number of trajects
        self.experiment_object_dict2 = {}
        self.data = {}  # Stores all quality scores of traject count

    def run_algorithm(self, **kwargs):
        """
        Runs experiments based on the selected algorithm and its parameters.
        This method handles both constructive and iterative algorithms by checking the type of the algorithm.
        """
        highest_quality = 0
        best_experiment_object = None

        # Put data in dict for more readability
        data = {
            'connections_file': self.connections_file,
            'locations_file': self.locations_file,
            'number_of_trajects': self.max_number_of_trajects,
            'max_time': self.max_time
        }

        # Update dict with parameters from main
        combined_data = {**data, **kwargs}

        # Loop through number of trajects as before
        for number_of_trajects in range(self.start_trajects, self.end_trajects + 1):
            qualities = []

            print(f"Starting experiments for {number_of_trajects} trajects...")

            for i in range(self.number_of_experiments1):
                # Initialize the experiment object based on the algorithm type
                if self.algorithm1 in [Randomise, GreedyLookahead, Greedy]:
                    experiment_object = self.algorithm1(**combined_data)

                # Run the experiment
                experiment_object.run()

                # Collect data
                quality, p = experiment_object.calculate_quality()
                qualities.append(quality)

                # Track the highest quality experiment
                if quality > highest_quality:
                    highest_quality = quality
                    best_experiment_object = experiment_object

                # Print progress every 100 iterations
                if (i + 1) % 100 == 0:
                    print(f"Progress: {i + 1}/{self.number_of_experiments1} iterations completed for {number_of_trajects} trajects.")

            # Update the best-yielding experiment for the current number of trajects
            self.experiment_object_dict[number_of_trajects] = best_experiment_object

            # Add qualities for all iterations for each traject number
            self.data[number_of_trajects] = qualities

        # Make a copy of experiment_object_dict for iterative algorithm
        self.experiment_object_dict2 = copy.deepcopy(self.experiment_object_dict)

        # If the algorithm is iterative (SimulatedAnnealing, HillClimber), apply the iterative optimization
        if self.algorithm2 in [SimulatedAnnealing, HillClimber]:
            for number_of_trajects, experiment_object in self.experiment_object_dict2.items():
                # Handle iterative algorithms like SimulatedAnnealing and HillClimber
                if self.algorithm2 == SimulatedAnnealing:
                    # If using SimulatedAnnealing, pass the temperature and alpha
                    algorithm_instance = self.algorithm2(experiment_object, combined_data.get('temperature', 1000), combined_data.get('alpha', 0.995))
                else:
                    # For HillClimber, pass the mutate_trajects_number and mutate_tracks_number
                    algorithm_instance = self.algorithm2(experiment_object, combined_data.get('num_trajects', 1), combined_data.get('num_tracks', 1))

                # Run the new experiment
                algorithm_instance.run(self.number_of_experiments2, verbose=True)

                # Update the dictionary with the optimized experiment
                optimized_train_table = algorithm_instance.train_table
                self.experiment_object_dict2[number_of_trajects] = optimized_train_table

    def save_all_collected_data(self, filename):
        """
        Saves a CSV file of all the collected data.
        """
        csv_filename = f"output/{filename}_allquality_data.csv"
        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            header = ["Number of Trajects"]

            # Use enumerate to generate headers
            for i, _ in enumerate(range(self.number_of_experiments1)):
                header.append(f"Quality Score {i + 1}")

            writer.writerow(header)

            # Add the data to rows in the csv file
            for number_of_trajects, qualities in self.data.items():
                row = [number_of_trajects] + qualities
                writer.writerow(row)

        print(f"Collected data saved as {csv_filename}")

    def save_all_objects(self, algorithm, data):
        """
        Saves the result of every experiment and visualises it.
        """
        for number_of_trajects, experiment_object in data.items():
            save_results(experiment_object, number_of_trajects, algorithm)

    def box_plot(self, filename=None):
        """
        Create a box plot and if filename exists, a PNG of the boxplot will be saved in the output folder.
        """
        if not self.data:
            print("No distribution available")
            return

        plt.boxplot(self.data.values(), labels=self.data.keys())
        plt.xlabel("Number of Trajects")
        plt.ylabel("Quality Score")
        plt.title(f"Box plot of experiment data, {self.number_of_experiments1} iterations from {self.start_trajects} till {self.end_trajects} trajects")

        if filename:
            plt.savefig(f"output/{filename}.png")
            print(f"Boxplot saved as {filename}")

        if filename is None:
            plt.show()
