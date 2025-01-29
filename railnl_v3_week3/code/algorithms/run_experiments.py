import matplotlib.pyplot as plt
from code.algorithms.experiment import Experiment
from code.classes.visualisation import Visualisation
from code.algorithms.randomise import Randomise
from code.classes.helper_functions import save_results
from code.algorithms.hillclimber import HillClimber
from code.algorithms.simulatedannealing import SimulatedAnnealing
from code.algorithms.greedy import Greedy
from code.algorithms.greedy import GreedyLookahead


class RunExperiments():
    def __init__(self, connections_file, locations_file, max_number_of_trajects, max_time, number_of_experiments1, number_of_experiments2, algorithm1_type, algorithm2_type, start_trajects = 7, end_trajects = 17, use_randomise = False):
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

        self.experiment_object_dict = {} #stores the best experiment objects for each number of trajects

        # List of lists of qualities
        # e.g. [traject1_data, traject2_data] with traject1_data = [experiment1_quality, experiment2_quality]
        self.data = {} #stores all quality scores of traject count

    def run_first_algorithm(self):
        """ Runs all experiments and collects data. Saves best quality experiment too.
        """
        print(f"Starting {str(self.algorithm1)} for {self.number_of_experiments1} iterations per traject number.")

        for number_of_trajects in range(self.start_trajects, self.end_trajects + 1):
            highest_quality = 0
            qualities = []
            best_experiment_object = None

            print(f"Starting experiments for {number_of_trajects} trajects...")

            for i in range(self.number_of_experiments1):
                # checks if an object has a randomise atribute
                if 'use_randomise' in self.algorithm1.__init__.__code__.co_varnames:
                    experiment_object = self.algorithm1(self.connections_file, self.locations_file, number_of_trajects, self.max_time, use_randomise = self.use_randomise)
                else:
                    experiment_object = self.algorithm1(self.connections_file, self.locations_file, number_of_trajects, self.max_time)

                # Initialize the experiment object
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

            print(f"Experiment {str(self.algorithm1)} has finished!")


    def save_all_objects(self, state_name, algorithm):
        """

        """
        for traject_count, experiment_object in self.experiment_object_dict.items():
            save_results(experiment_object, traject_count, state_name, algorithm)


    def run_second_algorithm(self, temperature):
        """
        Run second algorithm
        """
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

    def box_plot(self, filename = None):
        """
        Create a box plot and if filename exist, png of boxplot will be saved in output folder
        """

        # check if self.data is empty
        if not self.data:
            print("no distribution availible")
            return

        # create boxplot of colected data
        plt.boxplot(self.data.values(), labels = self.data.keys())
        plt.xlabel("Number of trajects")
        plt.ylabel("Quality score")
        plt.title(f"Box plot of experiment data, {self.number_of_experiments1} iterations from {self.start_trajects} till {self.end_trajects} trajects ")

        if filename:
            plt.savefig(f"output/{filename}.png")
            print(f"Boxplot saved as {filename}")

        if filename == None:
            plt.show()

    # def visualise(self):
    #     self.experiment_object_dict.visualisation()
    # def visualise_experiment(self, filename = None):
    #
    #     # check if there are results in experiment_object_dict
    #     if not self.experiment_object_dict:
    #         print("there is no best experiment so no visualisation possible")
    #         return
    #
    #     for number_of_trajects, experiment_object in self.experiment_object_dict.items():
    #         visualisation = Visualisation(experiment_object.stations_dict, experiment_object.connections_dict, experiment_object.traject_list)
    #         if filename:
    #             visualization_filename = f"output/{filename}_visualization.png"
    #             visualisation.save_visualisation(visualization_filename)
    #         if filename == None:
    #             visualisation.show_visualisation()
    # #

    # def create_boxplot(self):
    #     """ Display data as boxplot.
    #     """
    #     plt.boxplot(self.data)
    #     plt.xlabel("Number of trajects")
    #     plt.ylabel("Quality score")
    #     plt.title(f"Box plot of experiment data (N = {self.number_of_experiments*self.max_number_of_trajects})")
    #     plt.show()
