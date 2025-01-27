
import matplotlib.pyplot as plt
from code.algorithms.experiment import Experiment
from code.algorithms.randomise import Randomise


class RunExperiments():
    def __init__(self, connections_file, locations_file, max_number_of_trajects, max_time, number_of_experiments, algorithm_type = Randomise):
        self.connections_file = connections_file
        self.locations_file = locations_file
        self.max_number_of_trajects = max_number_of_trajects
        self.max_time = max_time
        self.number_of_experiments = number_of_experiments
        self.algorithm = algorithm_type
        self.best_yielding_experiment = None
        # List of lists of qualities
        # e.g. [traject1_data, traject2_data] with traject1_data = [experiment1_quality, experiment2_quality]
        self.data = {}

    def run(self):
        """ Runs all experiments and collects data. Saves best quality experiment too.
        """
        highest_quality = 0

        for number_of_trajects in range(7, self.max_number_of_trajects+1):
            qualities = []
            print(f"Starting experiments for {number_of_trajects} trajects...")

            for i in range(self.number_of_experiments):
                experiment_object = self.algorithm(self.connections_file, self.locations_file, number_of_trajects, self.max_time)

                # Run experiment
                experiment_object.run()

                # Print progress every 100 iterations
                if (i + 1) % 100 == 0:
                    print(f"Progress: {i + 1}/{self.number_of_experiments} iterations completed for {number_of_trajects} trajects.")

                # Collect data
                quality, p = experiment_object.calculate_quality()
                print(quality)
                qualities.append(quality)

                if quality > highest_quality:
                    highest_quality = quality
                    self.best_yielding_experiment = experiment_object

            # Add to dictionary
            self.data[number_of_trajects] = qualities

    def to_csv(self):
        self.best_yielding_experiment.output_to_csv()

    def visualise(self):
        self.best_yielding_experiment.visualisation()

    def print(self):
        self.best_yielding_experiment.print_output()

        return best_yielding_experiment

    def create_boxplot(self):
        """ Display data as boxplot.
        """
        plt.boxplot(self.data)
        plt.xlabel("Number of trajects")
        plt.ylabel("Quality score")
        plt.title(f"Box plot of experiment data (N = {self.number_of_experiments*self.max_number_of_trajects})")
        plt.show()
