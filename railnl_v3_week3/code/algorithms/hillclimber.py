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

        self.train_table = train_table  # Keeping the original train_table for reference
        self.value = train_table.calculate_quality()[0]


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
        random_traject_index = random.randint(0, len(new_table.traject_list) -1)

        # Generate a new random traject
        start_location = random.choice(list(new_table.stations_dict.keys()))  # Random start station

        # Create a new traject using Traject2
        new_traject = Traject2(start_location, new_table.color_list[random_traject_index])

        # Simulate movement for the new traject to make it valid
        while not new_traject.finished:
            new_table.movement(new_traject)

        # Replace the old traject with the new one
        new_table.traject_list[random_traject_index] = new_traject


    def mutate_track(self, new_table, number_of_tracks=1):
        """
        Mutates one or multiple connections within a traject and reroutes the traject.
        """
        random_traject_index = random.randint(0, len(new_table.traject_list) - 1)
        traject = new_table.traject_list[random_traject_index]

        # Ensure the traject has connections to remove
        if traject.connection_history:
            for _ in range(number_of_tracks):
                # Randomly choose to remove either the first or the last connection
                remove_choice = random.choice(["first", "last"])

                if remove_choice == "first":
                    # Remove the first connection and associated station
                    removed_connection = traject.connection_history.pop(0)
                    removed_station = traject.station_history.pop(0)
                    traject_time_to_subtract = new_table.connections_dict[removed_connection].time  # Extract time from the connection dict
                    traject.traject_time -= int(float(traject_time_to_subtract))  # Subtract the time from the total
                else:
                    # Remove the last connection and associated station
                    removed_connection = traject.connection_history.pop()
                    removed_station = traject.station_history.pop()
                    traject_time_to_subtract = new_table.connections_dict[removed_connection].time  # Extract time from the connection dict
                    traject.traject_time -= int(float(traject_time_to_subtract))  # Subtract the time from the total

        # Set the traject to unfisshed so we can use movement function
        traject.finished = False
        # Now use the movement function to reroute the traject
        new_table.movement(traject)


    def mutate_table(self, new_table, number_of_trajects=1, number_of_tracks=1):
        """
        Changes a random traject in the train table with a randomly generated traject.
        """
        for _ in range(number_of_trajects):
            #self.mutate_traject(new_table)
            self.mutate_track(new_table, number_of_tracks)

    def run(self, iterations, verbose=False, mutate_trajects_number=1, mutate_tracks_number=1):
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
            self.mutate_table(new_table, number_of_trajects=mutate_trajects_number, number_of_tracks=mutate_tracks_number)
            # Evalute new train table
            self.check_solution(new_table)

        # Heb nu hier de output/visualization want als ik deze in main call gebruikt hij nog niet de juiste waardes
        self.train_table.print_output()
        self.train_table.visualisation()
