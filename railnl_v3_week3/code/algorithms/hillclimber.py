import copy
import random
from code.algorithms.experiment import Experiment
from code.algorithms.randomise import Randomise
from code.algorithms.run_experiments import RunExperiments
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.visualisation import Visualisation
from code.classes.traject2 import Traject2



class HillClimber(Experiment):
    """
    The HillClimber class optimizes a solution by iteratively replacing random tracks
    in the train table with new random tracks. Improvements or equivalent solutions are kept.
    """

    def __init__(self, train_table,):
        """
        Initializes the HillClimber with a complete train table solution.
        """
        if not train_table.is_solution():
                raise Exception("HillClimber requires a complete solution.")

        self.train_table = copy.deepcopy(train_table)  # Keeping the original train_table for reference
        self.value = train_table.calculate_quality()[0]

        # ? do i need ?
        # self.best_solution = copy.deepcopy(train_table)
        # self.best_score = self.evaluate_solution(train_table)

    def check_solution(self, new_table):
        """
        Calculates the quality (K) of the train table solution using the quality formula.
        """
        new_value = new_table.calculate_quality()[0]
        old_value = self.value

        # We are looking for maps that cost less!
        if new_value >= old_value:
            self.train_table = new_table
            self.value = new_value

    def mutate_traject(self, new_table):
        """
        Mutates the current solution by replacing one random traject in the experiment
        with a newly generated random one.
        """
        # Select index of a random traject to replace
        random_traject_index = random.randint(0, len(new_table.traject_list) - 1)

        # Generate a new random traject
        start_location = random.choice(list(new_table.stations_dict.keys()))  # Random start station

        # Create a new traject using Traject2
        new_traject = Traject2(start_location, new_table.color_list[random_traject_index])

        # Simulate movement for the new traject to make it valid
        while not new_traject.finished:
            new_table.movement(new_traject)

        # Replace the old traject with the new one
        new_table.traject_list[random_traject_index] = new_traject

    def mutate_track(self):
        pass

    def mutate_table(self, new_table, number_of_trajects=1):
        """
        Changes a random traject in the train table with a randomly generated traject.
        """
        for _ in range(number_of_trajects):
            self.mutate_traject(new_table)



    def run(self, iterations, verbose=False, mutate_trajects_number=1):
        """
        Runs the HillClimber algorithm for the specified number of iterations.
        """
        self.iterations = iterations
        for iteration in range(iterations):
            print(f'Iteration {iteration}/{iterations}, current value: {self.value}') if verbose else None

            # Generate a neighboring solution
            new_table = copy.deepcopy(self.train_table)
            new_table.reset_connection_frequencies()
            # Evaluate the neighboring solution
            self.mutate_table(new_table, number_of_trajects=mutate_trajects_number)

            self.check_solution(new_table)

        # Heb nu hier de output/visualization want als ik deze in main call gebruikt hij nog niet de juiste waardes
        self.train_table.print_output()
        self.train_table.visualisation()
