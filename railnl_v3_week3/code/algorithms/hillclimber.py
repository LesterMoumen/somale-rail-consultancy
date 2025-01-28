import copy
import random
from code.algorithms.experiment import Experiment
from code.algorithms.randomise import Randomise
# from code.algorithms.run_experiments import RunExperiments
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.visualisation import Visualisation
from code.classes.traject2 import Traject2
from code.classes.trajectanalyzer import TrajectAnalyzer



class HillClimber(Experiment):
    """
    The HillClimber class optimizes a solution by iteratively replacing random tracks
    in the train table with new random tracks. Improvements or equivalent solutions are kept.
    """

    def __init__(self, train_table):
        """
        Initializes the HillClimber with a complete train table solution.
        """
        #if not train_table.is_solution():
        #        raise Exception("HillClimber requires a complete solution.")

        self.train_table = copy.deepcopy(train_table)  # Keeping the original train_table for reference
        self.value = train_table.calculate_quality()[0]
        # Initialize TrajectAnalyzer with necessary data
        self.traject_analyzer = TrajectAnalyzer(
            self.train_table.stations_dict,
            self.train_table.connections_dict,
            self.train_table.traject_list,
            self.train_table.connections_set
        )

        # Access the used stations
        self.used_stations = self.traject_analyzer.used_stations

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


    def clear_traject(self, traject, new_table):
        while traject.connection_history:
            self.clear_connection(traject, new_table)


    def clear_connection(self, traject, new_table, index=None):
        """
        Removes a connection from the traject at the specified index.
        If no index is provided, removes the last connection.
        """
        if traject.connection_history:
            # Remove connection by index or last connection
            if index is not None:
                removed_connection = traject.connection_history.pop(index)
                removed_station = traject.station_history.pop(index)
            else:
                removed_connection = traject.connection_history.pop()
                removed_station = traject.station_history.pop()

            # Update connection usage count
            new_table.connections_dict[removed_connection].times_used -= 1

            # Subtract the connection's time from the traject's total time
            traject_time_to_subtract = new_table.connections_dict[removed_connection].time
            traject.traject_time -= int(float(traject_time_to_subtract))
        else:
            raise ValueError("Traject has no connections to remove.")


    def mutate_traject(self, new_table):
        """
        Mutates the current solution by replacing one random traject in the experiment
        with a newly generated random one.
        """
        # Select index of a random traject to replace
        random_traject_index = random.randint(0, len(new_table.traject_list) -1)
        traject = new_table.traject_list[random_traject_index]

        self.clear_traject(traject, new_table)

        available_stations = list(set(new_table.stations_dict.keys()) - self.used_stations)
        if available_stations:
            # Generate a new random traject
            start_location = random.choice(available_stations)  # Random start station
        else:
            # Fallback: reroute to any used station
            used_stations = list(self.used_stations)  # Assuming self.used_stations is a set of used station names
            start_location = random.choice(used_stations)

        # Create a new traject using Traject2
        new_traject = Traject2(start_location, new_table.color_list[random_traject_index])

        # Simulate movement for the new traject to make it valid
        while not new_traject.finished:
            new_table.movement(new_traject)

        # Replace the old traject with the new one
        new_table.traject_list[random_traject_index] = new_traject


    def mutate_track(self, new_table, number_of_tracks):
        """
        Mutates one or multiple connections within a traject and reroutes the traject.
        """
        random_traject_index = random.randint(0, len(new_table.traject_list) - 1)
        traject = new_table.traject_list[random_traject_index]

        # Remove specified number of connections
        for _ in range(number_of_tracks):
            if traject.connection_history:
                # Randomly choose to remove either the first or the last connection
                if random.choice(["first", "last"]) == "first":
                    self.clear_connection(traject, new_table, index=0)
                else:
                    self.clear_connection(traject, new_table)

        # Determine the starting point for rerouting
        start_index = random.choice([0, -1])
        if start_index == 0:  # Start from the tail
            traject.location = traject.station_history[start_index]
            traject.station_history.reverse()
        else:  # Start from the head
            traject.location = traject.station_history[-1]

        # Mark the traject as unfinished
        traject.finished = False

        # Reroute the traject using the movement function
        while not traject.finished:
            new_table.movement(traject)


    def mutate_table(self, new_table, number_of_trajects, number_of_tracks):
        """
        Changes a random traject in the train table with a randomly generated traject.
        """
        for _ in range(number_of_trajects):
            self.mutate_traject(new_table)
            self.mutate_track(new_table, number_of_tracks)


    def run(self, iterations, verbose=False, mutate_trajects_number=1, mutate_tracks_number=5):
        """
        Runs the HillClimber algorithm for the specified number of iterations.
        """

        for iteration in range(iterations):
            print(f'Iteration {iteration}/{iterations}, current value: {self.value}') if verbose else None

            # Generate a neighboring solution
            new_table = copy.deepcopy(self.train_table)

            # Update used stations after mutation
            self.traject_analyzer = TrajectAnalyzer(
                new_table.stations_dict,
                new_table.connections_dict,
                new_table.traject_list,
                new_table.connections_set
            )

            self.used_stations = self.traject_analyzer.used_stations

            # Evaluate the neighboring solution
            self.mutate_table(new_table, number_of_trajects=mutate_trajects_number, number_of_tracks=mutate_tracks_number)
            # Evalute new train table
            self.check_solution(new_table)


        # Heb nu hier de output/visualization want als ik deze in main call gebruikt hij nog niet de juiste waardes
        # self.train_table.print_output()
        # self.train_table.visualisation()
