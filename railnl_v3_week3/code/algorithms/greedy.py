import copy
import random
from code.algorithms.experiment import Experiment
from code.classes.traject2 import Traject2
from code.classes.trajectanalyzer import TrajectAnalyzer
import code.classes.helper_functions as helper
from code.algorithms.randomise import Randomise

class Greedy(Experiment):
    def start_station(self):
        """
        Return random starting station from list of stations.
        """

        ta = TrajectAnalyzer(self.stations_dict, self.connections_dict, self.traject_list, self.connections_set)
        next_start_station = ta.find_next_start_location()

        return next_start_station

    def get_next_connection(self, traject_object, connection_options):
        """
        Returns the next connection which has the highest quality.
        """
        best_quality = float('-inf')
        best_connection = None
        best_next_station = None

        # loops through all possible connections
        for connecting_station, time in connection_options.items():

            connection = helper.sorted_connection(traject_object.location, connecting_station)

            # Get next connection quality
            # Connection used is used to calculate p in quality
            connections_used = (self.get_connection_histories()).union({connection})
            total_time = self.get_total_time() + float(time)
            next_connection_quality, p = self.calculate_quality(connections_used, total_time)

            # Saves the best quality and connection
            if next_connection_quality > best_quality:
                best_quality = next_connection_quality
                best_connection = connection
                best_next_station = connecting_station

        return best_connection, best_next_station

    def movement(self, traject_object):
        """
        Movement of traject_object to next station
        """

        # Get dict of valid connections (within max time) from current location
        valid_connection_options = self.valid_connection_options(traject_object)

        if valid_connection_options:
            next_connection, next_start_station = self.get_next_connection(traject_object, valid_connection_options)
            new_time = self.connections_dict[next_connection].time
            traject_object.update(next_connection, next_start_station, new_time)
            self.connections_dict[next_connection].update_used()

        else:
            traject_object.finished = True

    def initialize_traject(self, color_list_i):

        start_loca = self.start_station()

        if isinstance(start_loca, str):
            start_location = start_loca
            next_connecting_station = None
        else:
            start_location, next_connecting_station = self.start_station()

        traject_object = Traject2(start_location, self.color_list[color_list_i])
        self.traject_list.append(traject_object)

        # if traject_analyzer is used next_connecting_station != None than use the traject_analyzer as next_connecting_station
        # Detects if start_location is a dead end, because it has a next_connecting_station
        if next_connecting_station:
            # Performs the first movement to the next_connecting_station
            next_station, time = next_connecting_station
            connection = helper.sorted_connection(start_location, next_station)
            traject_object.update(connection, next_station, time)
            self.connections_dict[connection].update_used()

        return traject_object


    def run(self):
        """ Run the greedy algorithm.
        """

        for i in range(self.number_of_trajects):
            traject_object = self.initialize_traject(i)

            # Continues running until traject is finished
            while not traject_object.finished:
                self.movement(traject_object)

            connections_visited = self.get_connection_histories()
            total_time = self.get_total_time()
            quality, p = self.calculate_quality(connections_visited, total_time)

            if p == 1:
                print("All connections have been visited")
                break


class GreedyLookahead(Greedy):
    def __init__(self, connections_file, locations_file, number_of_trajects, max_time, lookahead_depth=1, use_randomise=False):
        """
        initialize the GreedyLookahead algorithm
        - It has a lookahead depth of 3
        - It has the option to use the Random algorithm for a start_station
        """
        super().__init__(connections_file, locations_file, number_of_trajects, max_time)
        self.lookahead_depth = lookahead_depth
        self.use_randomise = use_randomise

        self.connections_file = connections_file
        self.locations_file = locations_file
        self.number_of_trajects = number_of_trajects
        self.max_time = max_time

        # Use randomise algorithm if use_randomise = True
        self.randomise = Randomise(self.connections_file, self.locations_file, self.number_of_trajects, self.max_time) if self.use_randomise else None

    def start_station(self):
        '''
        Start station for GreedyLookahead.
        - if self.use_randomise is True it uses random start station else uses the traject analyzer heuristic
        '''
        if self.use_randomise and self.randomise:
            return self.randomise.start_station(self.stations_dict.keys())
        else:
            ta = TrajectAnalyzer(self.stations_dict, self.connections_dict, self.traject_list, self.connections_set)
            return ta.find_next_start_location()


    def simulate_best_path(self, current_station, depth, visited_connections, total_quality, traject_object):
        """
        Recursively find the best path starting from the current station and explores the best path to a specified depth.
        Return the best path and its quality
        """
        # if there are no lookahead depths anymore, return a empty path and quality
        if depth == 0:
            return [], total_quality

        best_quality = float('-inf')
        best_path = []

        # valid connection option within max time
        connection_options = self.valid_connection_options(traject_object)

        for next_station, travel_time in connection_options.items():
            connection = helper.sorted_connection(current_station, next_station)

            # calculate the quality of the new path
            new_visited_connections = visited_connections.union({connection})
            total_time = self.get_total_time() + float(travel_time)
            next_connection_quality, p = self.calculate_quality(new_visited_connections, total_time)
            new_quality = total_quality + next_connection_quality

            # Recursively explores the next depth
            trail_path, trail_quality = self.simulate_best_path( next_station, depth - 1, new_visited_connections, new_quality, traject_object)

            # saves the best path if it has a higher quality
            if trail_quality > best_quality and trail_quality > float('-inf'):
                best_quality = trail_quality
                best_path = [next_station] + trail_path

        return best_path, best_quality

    def movement(self, traject_object):
        """
        Move the traject object to the next station using lookahead. If there are no valid connections the traject will be marked as finished.
        """

        valid_connections = self.valid_connection_options(traject_object)

        if valid_connections:
            best_path, best_quality = self.simulate_best_path(traject_object.location, depth=self.lookahead_depth, visited_connections=set(traject_object.connection_history), total_quality=0, traject_object=traject_object)

            if best_path:
                next_station = best_path[0]

                connection = helper.sorted_connection(traject_object.location, next_station)
                time = self.connections_dict[connection].time
                total_time_traject = float(time) + traject_object.traject_time

                traject_object.update(connection, next_station, time)
                self.connections_dict[connection].update_used()
            else:
                traject_object.finished = True
        else:
            traject_object.finished = True
