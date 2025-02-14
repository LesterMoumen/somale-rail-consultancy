import copy
import random
import csv
from code.classes.experiment import Experiment
from code.algorithms.randomise import Randomise
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.visualisation import Visualisation
from code.classes.traject import Traject
from code.classes.trajectanalyzer import TrajectAnalyzer



class HillClimber(Experiment):
    """
    The HillClimber class optimizes a solution by iteratively replacing random tracks
    in the train table with new random tracks. Improvements or equivalent solutions are kept.
    """

    def __init__(self, train_table, mutate_trajects_number, mutate_tracks_number, number_of_trajects):
        """
        Initializes the HillClimber with a complete train table solution.
        """


        self.train_table = copy.deepcopy(train_table)  # Keeping the original train_table for reference
        self.train_table.number_of_trajects = number_of_trajects  # Couldn't fix the error
        self.value = train_table.calculate_quality()[0]

        # Access the used stations
        self.used_stations = self.update_used_stations()

        # Parameters
        self.mutate_trajects_number = mutate_trajects_number
        self.mutate_tracks_number = mutate_tracks_number

        # List to store the quality and parameters for each iteration
        self.iteration_history = []

    def update_used_stations(self):
        """
        Re-initializes the TrajectAnalyzer and updates used stations.
        This method is called after every mutation to reflect the new train table state.
        """
        self.traject_analyzer = TrajectAnalyzer(
            self.train_table.stations_dict,
            self.train_table.connections_dict,
            self.train_table.traject_list,
            self.train_table.connections_set
        )

        return self.traject_analyzer.used_stations

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
        """
        Clears the whole traject from our data using clear_connection method.
        """
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

        # Delete the traject from data
        self.clear_traject(traject, new_table)

        # Prioritizes start station that has not been used yet
        available_stations = list(set(new_table.stations_dict.keys()) - self.used_stations)
        if available_stations:
            # Generate a new random traject
            start_location = random.choice(available_stations)  # Random start station

        # If every station is used reroute to any used station
        else:
            used_stations = list(self.used_stations)  # Assuming self.used_stations is a set of used station names
            start_location = random.choice(used_stations)

        # Create a new traject using Traject
        new_traject = Traject(start_location, new_table.color_list[random_traject_index])

        # Simulate movement for the new traject to make it valid
        while not new_traject.finished:
            new_table.movement(new_traject)

        # Replace the old traject with the new one
        new_table.traject_list[random_traject_index] = new_traject


    def mutate_track(self, new_table):
        """
        Mutates one or multiple connections within a traject and reroutes the traject.
        """
        random_traject_index = random.randint(0, len(new_table.traject_list) - 1)
        traject = new_table.traject_list[random_traject_index]

        # Remove specified number of connections
        for _ in range(self.mutate_tracks_number):
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


    def mutate_table(self, new_table):
        """
        Changes a random traject in the train table with a randomly generated traject.
        """
        for _ in range(self.mutate_trajects_number):
            self.mutate_traject(new_table)

        # FF KIJKEN WAAR DIT BEST KAN STAAN
        self.mutate_track(new_table)

    def store_iteration_data(self, iteration):
         # Store parameters and quality at each iteration
        iteration_data = {
            'iteration': iteration,
            'value': self.value,
            'mutate_trajects_number': self.mutate_trajects_number,
            'mutate_tracks_number': self.mutate_tracks_number
        }
        self.iteration_history.append(iteration_data)


    def save_all_iterations_data(self, filename):
        """
        Saves a CSV file of all the collected data, including iteration parameters and quality scores.
        """
        print(f"Saving file for traject count: {self.train_table.number_of_trajects}")

        csv_filename = f"output/{filename}trajectnumber{self.train_table.number_of_trajects}._mutate{self.mutate_tracks_number}tracks_mutate{self.mutate_trajects_number}trajects_quality_data.csv"
        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Add header for the number of trajects, iteration parameters, and quality score
            header = ["Iteration", "Quality Score", "Mutate Trajects Number", "Mutate Tracks Number"]

            writer.writerow(header)

            # Add the iteration data for each experiment
            for iteration_data in self.iteration_history:
                row = [
                    iteration_data['iteration'],
                    iteration_data['value'],
                    iteration_data['mutate_trajects_number'],
                    iteration_data['mutate_tracks_number']
                ]
                writer.writerow(row)

        print(f"Collected data saved as {csv_filename}")


    def run(self, iterations, verbose=False):
        """
        Runs the HillClimber algorithm for the specified number of iterations.
        """

        for iteration in range(iterations):
            print(f'Iteration {iteration}/{iterations}, current value: {self.value}') if verbose else None

            # Generate a neighboring solution
            new_table = copy.deepcopy(self.train_table)

            # Update used stations after mutation
            self.update_used_stations()

            # Evaluate the neighboring solution
            self.mutate_table(new_table)
            # Evalute new train table
            self.check_solution(new_table)

            self.store_iteration_data(iteration)

        self.save_all_iterations_data(HillClimber.__name__)
