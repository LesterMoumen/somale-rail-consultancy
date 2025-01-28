import copy
import random
from code.algorithms.experiment import Experiment
from code.classes.traject2 import Traject2
from code.classes.trajectanalyzer import TrajectAnalyzer
import code.classes.helper_functions as helper

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
        - It avoids connections which already has been visited
        """
        best_quality = float('-inf')
        best_connection = None
        best_next_station = None

        # Loop over valid connections
        for connecting_station, time in connection_options.items():
            connection = helper.sorted_connection(traject_object.location, connecting_station)

            # Get next connection quality
            # Connection used is used to calculate p in quality
            connections_used = (self.get_connection_histories()).union({connection})
            total_time = self.get_total_time() + float(time)
            next_connection_quality, p = self.calculate_quality(connections_used, total_time)


            if next_connection_quality > best_quality:
                best_quality = next_connection_quality
                best_connection = connection
                best_next_station = connecting_station

        #if best_connection and best_next_station:
        return best_connection, best_next_station
        #else:
        #    return None

    def movement(self, traject_object):
        """
        Movement of traject_object to next station
        """
        # Get dict of valid connections (within max_min) from current location
        valid_connection_options = self.valid_connection_options(traject_object)

        if valid_connection_options:
            next_connection, next_start_station = self.get_next_connection(traject_object, valid_connection_options)
            new_time = self.connections_dict[next_connection].time
            traject_object.update(next_connection, next_start_station, new_time)

            self.connections_dict[next_connection].update_used()
        else:
            traject_object.finished = True

    def initialize_traject(self, color_list_i):
        start_location, next_connecting_station = self.start_station()

        traject_object = Traject2(start_location, self.color_list[color_list_i])
        self.traject_list.append(traject_object)

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
        print()
        print("Start running Greedy2")
        #print(self.number_of_trajects)
        print()
        print("Starting for i in range loop")
        for i in range(self.number_of_trajects):
            print("Initialize traject", i+1)
            traject_object = self.initialize_traject(i)
            print("Initialize traject", i+1, "finished!")
            print()

            # Continues running until traject is finished
            while not traject_object.finished:
                self.movement(traject_object)


class GreedyLookahead(Greedy):
    def __init__(self, connections_file, locations_file, number_of_trajects, max_time, lookahead_depth=3):
        super().__init__(connections_file, locations_file, number_of_trajects, max_time)
        self.lookahead_depth = lookahead_depth

    def simulate_best_path(self, current_station, depth, visited_connections, total_quality):
        """
        Recursively find the best path starting from the current station.
        """
        if depth == 0:
            return [], total_quality

        best_quality = float('-inf')
        best_path = []

        connection_options = self.stations_dict[current_station].connections

        for next_station, time in connection_options.items():
            connection = helper.sorted_connection(current_station, next_station)

            new_visited_connections = visited_connections.union({connection})
            total_time = self.get_total_time() + float(time)


            next_connection_quality, p = self.calculate_quality(new_visited_connections, total_time)

            new_quality = total_quality + next_connection_quality


            trail_path, trail_quality = self.simulate_best_path( next_station, depth - 1, new_visited_connections, new_quality)

            # if trail_quality > best_quality:
            if trail_quality > best_quality and trail_quality > float('-inf'):
                # print("sub quality/ bestquality", trail_quality)
                best_quality = trail_quality
                best_path = [next_station] + trail_path


        return best_path, best_quality

    def movement(self, traject_object):
        """
        Move the traject object to the next station using lookahead.
        """
        valid_connections = self.valid_connection_options(traject_object)

        if valid_connections:
            best_path, best_quality = self.simulate_best_path(traject_object.location, depth=self.lookahead_depth, visited_connections=set(traject_object.connection_history), total_quality=0)

            if best_path:
                next_station = best_path[0]

                connection = helper.sorted_connection(traject_object.location, next_station)
                time = self.connections_dict[connection].time



                traject_object.update(connection, next_station, time)
                self.connections_dict[connection].update_used()
            else:
                # print(f"[DEBUG] No valid path from {traject_object.location}. Traject finished.")

                traject_object.finished = True
        else:
            # print(f"[DEBUG] No valid connections from {traject_object.location}. Traject finished.")

            traject_object.finished = True
