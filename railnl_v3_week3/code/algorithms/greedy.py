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

        # print("Dead ends:", ta.find_dead_ends())
        # print("Odds:", ta.find_odd_connections())
        # start_station_random = random.choice(list(list_of_stations))
        # print("Start Location:", next_start_station)
        # print()
        return next_start_station #_random

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
            connection_histories = (self.get_connection_histories()).union({connection}) #.add(connection) #.add(connection)
            total_time = self.get_total_time() + float(time)
            next_connection_quality, p = self.calculate_quality(connection_histories, total_time)
            #print(f"Connection {connection}'s score: {next_connection_quality}")

            #used_connections = self.connections_dict[connection].times_used
            #print("used connections", used_connections)

            # If the connection has already been used it will give a penalty
            #if used_connections >= 1:
            #    next_connection_quality -= 1000

            if next_connection_quality > best_quality:
                best_quality = next_connection_quality
                best_connection = connection
                best_next_station = connecting_station
                #print("      New best:", best_connection)

            #print()

        if best_connection and best_next_station:
            return best_connection, best_next_station
        else:
            return None

    def movement(self, traject_object):
        """
        Movement of traject_object to next station
        """
        # Get dict of valid connections (within max_min) from current location
        valid_connection_options = self.valid_connection_options(traject_object)

        if valid_connection_options:
            next_connection, next_station = self.get_next_connection(traject_object, valid_connection_options)
            #print("Next station:", next_station)

            time = self.connections_dict[next_connection].time
            traject_object.update(next_connection, next_station, time)
            # print("next station", next_station)
            # print()
            # print("next connection", next_connection)
            # print()

            self.connections_dict[next_connection].update_used()
        else:
            traject_object.finished = True

    def initialize_traject(self, color_list_i):
        start_location = self.start_station()
        traject_object = Traject2(start_location, self.color_list[color_list_i])
        self.traject_list.append(traject_object)

        return traject_object


    def run(self):
        """ Run the greedy algorithm.
        """
        #print(self.number_of_trajects)
        for i in range(self.number_of_trajects):
            #print()
            #print(f"Traject {i+1}")
            traject_object = self.initialize_traject(i)

            # Continues running until traject is finished
            while not traject_object.finished:
                #result = self.get_next_connection(traject_object)

                self.movement(traject_object)
                #if result is not None:
                #    best_connection, next_station = result
                #if best_connection is None:
                #    traject_object.finished = True
                #    break
                #self.movement(traject_object, best_connection, next_station)
            #print("Traject finished")


        #self.initialize_trajects()
        # for traject_object in self.traject_list:
        #     while not traject_object.finished:
        #         best_station = self.get_next_connection(traject_object)
        #         if best_station is None:
        #             traject_object.finished = True
        #             break
        #         self.movement(traject_object, best_station)



class GreedyLookahead(Greedy):
    def __init__(self, connections_file, locations_file, number_of_trajects, max_time, lookahead_depth=2):
        super().__init__(connections_file, locations_file, number_of_trajects, max_time)
        self.lookahead_depth = lookahead_depth

    def simulate_best_path(self, current_station, depth, visited_connections, total_quality):
        """
        Recursively find the best path starting from the current station.
        """
        # if there are no lookahead depths anymore, return a empty path and quality
        if depth == 0:
            return [], total_quality

        best_quality = float('-inf')
        best_path = []
        print(f"\n[DEBUG] Exploring station: {current_station} at depth {depth}")
        print(f"Visited connections so far: {visited_connections}")
        print(f"Total quality so far: {total_quality}")

        # connection options from the current station
        connection_options = self.stations_dict[current_station].connections

        for next_station, travel_time in connection_options.items():
            connection = helper.sorted_connection(current_station, next_station)

            new_visited_connections = visited_connections.union({connection})
            total_time = self.get_total_time() + float(travel_time)

            # calculate quality of the path
            next_connection_quality, p = self.calculate_quality(new_visited_connections, total_time)
            new_quality = total_quality + next_connection_quality

            # repeatatly exploring the next station until the depth is 0
            trail_path, trail_quality = self.simulate_best_path(next_station, depth - 1, new_visited_connections, new_quality)

            # update the best path and quality if current trail is better
            if trail_quality > best_quality and trail_quality > float('-inf'):
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
                print()
                connection = helper.sorted_connection(traject_object.location, next_station)
                time = self.connections_dict[connection].time
                # Debug: Log chosen path and quality
                print(f"Current Station: {traject_object.location}")
                print(f"Next Station: {next_station}")
                print(f"Connection: {connection}")
                print(f"Path Quality: {best_quality}")
                # print(f"Time: {time}, total time {self.get_total_time() + float(time)}")


                traject_object.update(connection, next_station, time)
                self.connections_dict[connection].update_used()
            else:
                traject_object.finished = True
                print()
        else:
            traject_object.finished = True
            print()
