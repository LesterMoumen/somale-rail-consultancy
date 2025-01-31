import random
from code.classes.experiment import Experiment
from code.classes.traject import Traject
from code.classes.trajectanalyzer import TrajectAnalyzer
import code.classes.helper_functions as helper
from code.algorithms.randomise import Randomise

class Greedy(Experiment):
    """
    The greedy algoritm calculates from every station the possible next connections and its quality.
    When a connection leads to a higher quality score, the traject will move to that station. Than from
    the this proces will repeat itselfs untill the max time of a traject is reached or if there are no availible
    connections left.
    """

    def __init__(self, connections_file, locations_file, number_of_trajects, max_time, use_randomise=False):
        super().__init__(connections_file, locations_file, number_of_trajects, max_time)

        # If self.use_randomise is True the starting station will use random algorithm
        self.use_randomise = use_randomise
        self.randomise = Randomise(connections_file, locations_file, number_of_trajects, max_time) if use_randomise else None

    def start_station(self):
        """
        Return a starting station using either Randomise or TrajectAnalyzer.
        """
        if self.use_randomise and self.randomise:
            return self.randomise.start_station(self.stations_dict.keys())
        else:
            ta = TrajectAnalyzer(self.stations_dict, self.connections_dict, self.traject_list, self.connections_set)
            return ta.find_next_start_location()

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
        Movement of traject_object to the next station
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
        """
        Initializes a new traject object and determines the start station using randomise or traject analyzer.
        """
        start_loca = self.start_station()

         # Randomise returns only the start station
        if isinstance(start_loca, str):
            start_location = start_loca
            next_connecting_station = None

        # TrajectAnalyzer returns start location and next connecting station
        else:
            start_location, next_connecting_station = start_loca

        traject_object = Traject(start_location, self.color_list[color_list_i])
        self.traject_list.append(traject_object)

        # if traject_analyzer is used next_connecting_station != None than use the traject_analyzer as next_connecting_station
        # Detects if start_location is a dead end, because it has a next_connecting_station
        if next_connecting_station:
            next_station, time = next_connecting_station
            connection = helper.sorted_connection(start_location, next_station)
            traject_object.update(connection, next_station, time)
            self.connections_dict[connection].update_used()

        return traject_object

    def run(self):
        """ Run the Greedy or GreedyLookahead algorithm.
        """

        for i in range(self.number_of_trajects):
            traject_object = self.initialize_traject(i)

            # Continues running until traject is finished
            while not traject_object.finished:
                self.movement(traject_object)

            connections_visited = self.get_connection_histories()
            total_time = self.get_total_time()
            quality, p = self.calculate_quality(connections_visited, total_time)

            # when p is 1 all connections are visited; the simulation stops.
            if p == 1:
                print("All connections have been visited")
                break


class GreedyLookahead(Greedy):
    """
    This algoritm will use a lookahead depth to simulate all paths from a start station and calculate the quality score from all paths.
    The best path will be saved and the traject will move to the next station, this is the first station in best path. When the traject is moved,
    the proces will repeat itselfs.
    """
    def __init__(self, connections_file, locations_file, number_of_trajects, max_time, lookahead_depth, use_randomise=False):
        """
        initialize the GreedyLookahead algorithm
        - It has a variable lookahead depth
        - It has the option to use a random start_station or use TrajectAnalyzer to determine the start station.
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
        Recursively find the best path starting from the current station and explores the best
        path (the path with the highest quality) to a specified depth.
        Return the best path and its quality.

        e.g.
        Den Helder --> Alkmaar = quality 3
        Alkmaar --> Hoorn = quality 10
        Hoorn --> Zaandam = quality 3

        Den helder --> Alkmaar = quality 3
        Alkmaar --> Castricum = quality 5
        Castricum --> Amsterdam Sloterdijk = quality 15

        Calculate both path quality and chooses next station with highest path quality.
        """
        # if there are no lookahead depths anymore, return a empty path and quality
        if depth == 0:
            return [], total_quality

        # initialize variables to track the best path and quality
        best_quality = float('-inf')
        best_path = []

        # get connection options from current station
        connection_options = self.stations_dict[current_station].connections

        # loops through all connection options
        for next_station, travel_time in connection_options.items():
            connection = helper.sorted_connection(current_station, next_station)

            # calculate the quality of the new connection and the path
            new_visited_connections = visited_connections.union({connection})
            total_time = self.get_total_time() + float(travel_time)
            next_connection_quality, p = self.calculate_quality(new_visited_connections, total_time)
            new_quality = total_quality + next_connection_quality

            # Recursively explores the next station and its quality
            trail_path, trail_quality = self.simulate_best_path(next_station, depth - 1, new_visited_connections, new_quality, traject_object)

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
