import matplotlib.pyplot as plt
from code.algorithms.experiment import Experiment
from code.algorithms.randomise import Randomise
from code.classes.helper_functions import save_results
from code.algorithms.hillclimber import HillClimber
from code.algorithms.simulatedannealing import SimulatedAnnealing


class RunExperiments():
    def __init__(self, connections_file, locations_file, max_number_of_trajects, max_time, number_of_experiments1, number_of_experiments2, algorithm1_type, algorithm2_type, use_randomise = False):
        self.connections_file = connections_file
        self.locations_file = locations_file
        self.max_number_of_trajects = max_number_of_trajects
        self.max_time = max_time
        self.number_of_experiments1 = number_of_experiments1
        self.number_of_experiments2 = number_of_experiments2
        self.algorithm1 = algorithm1_type
        self.algorithm2 = algorithm2_type
        self.use_randomise = use_randomise
        self.experiment_object_dict = {}

        # List of lists of qualities
        # e.g. [traject1_data, traject2_data] with traject1_data = [experiment1_quality, experiment2_quality]
        self.data = {}

    def run_first_algorithm(self):
        """ Runs all experiments and collects data. Saves best quality experiment too.
        """

        for number_of_trajects in range(11, 12): #self.max_number_of_trajects+1):
            highest_quality = 0
            qualities = []
            best_experiment_object = None

            print(f"Starting experiments for {number_of_trajects} trajects...")

            for i in range(self.number_of_experiments1):
                # Initialize the experiment object
                experiment_object = self.algorithm1(self.connections_file, self.locations_file, number_of_trajects, self.max_time)
                experiment_object.run()

                # Print progress every 100 iterations
                if (i + 1) % 100 == 0:
                    print(f"Progress: {i + 1}/{self.number_of_experiments1} iterations completed for {number_of_trajects} trajects.")

                # Collect data
                quality, p = experiment_object.calculate_quality()
                qualities.append(quality)

                if quality > highest_quality:
                    highest_quality = quality
                    best_experiment_object = experiment_object


            # Update the best-yielding experiment
            self.experiment_object_dict[number_of_trajects] = best_experiment_object

            # Add to dictionary
            self.data[number_of_trajects] = qualities


    def save_all_objects(self, state_name):
        for traject_count, experiment_object in self.experiment_object_dict.items():
            save_results(experiment_object, traject_count, state_name)


    def run_second_algorithm(self, temperature):
        for traject_count, experiment_object in self.experiment_object_dict.items():

            # If using SimulatedAnnealing, pass the temperature
            if self.algorithm2 == SimulatedAnnealing:
                algorithm = self.algorithm2(experiment_object, temperature)
            # Otherwise, use HillClimber (which doesn't need temperature)
            else:
                algorithm = self.algorithm2(experiment_object)

            # Run the new experiment
            algorithm.run(self.number_of_experiments2, verbose=True)

            # Update the dictionary with the modified experiment
            optimized_train_table = algorithm.train_table
            self.experiment_object_dict[traject_count] = optimized_train_table

    # def visualise(self):
    #     self.experiment_object_dict.visualisation()


    def create_boxplot(self):
        """ Display data as boxplot.
        """
        plt.boxplot(self.data)
        plt.xlabel("Number of trajects")
        plt.ylabel("Quality score")
        plt.title(f"Box plot of experiment data (N = {self.number_of_experiments*self.max_number_of_trajects})")
        plt.show()
