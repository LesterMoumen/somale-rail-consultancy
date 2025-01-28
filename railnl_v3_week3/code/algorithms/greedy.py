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

        print("Dead ends:", ta.find_dead_ends())
        print("Odds:", ta.find_odd_connections())
        # start_station_random = random.choice(list(list_of_stations))
        print("Start Location:", next_start_station)
        print()
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
    def __init__(self, connections_file, locations_file, number_of_trajects, max_time, lookahead_depth=1):
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

        # if current_station not in self.stations_dict:
        #     return [], total_quality

        connection_options = self.stations_dict[current_station].connections
        # print(f"Current Station: {current_station}, Depth: {depth}")
        # print("connection options", connection_options)
        # connection_options = self.valid_connections_options()

        for next_station, time in connection_options.items():
            connection = helper.sorted_connection(current_station, next_station)

            new_visited_connections = visited_connections.union({connection})
            total_time = self.get_total_time() + float(time)

            # if total_time > self.max_time:
            #     print(f"Path to {next_station} exceeds max_time. Skipping.")
            #     continue

            next_connection_quality, p = self.calculate_quality(new_visited_connections, total_time)

            new_quality = total_quality + next_connection_quality

            # print(f"Evaluating Path: {current_station} -> {next_station}")
            # print(f"Visited Connections: {new_visited_connections}")
            # print(f"New Quality: {new_quality}, calculate_quality score {next_connection_quality}")

            trail_path, trail_quality = self.simulate_best_path( next_station, depth - 1, new_visited_connections, new_quality
            )
            # total_quality_path = new_quality

            # if trail_quality > best_quality:
            if trail_quality > best_quality and trail_quality > float('-inf'):
                # print("sub quality/ bestquality", trail_quality)
                best_quality = trail_quality
                best_path = [next_station] + trail_path
        print(f"Best Path from {current_station}: {best_path} with Quality: {best_quality}")
        print()
        print()

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
                print()
                connection = helper.sorted_connection(traject_object.location, next_station)
                time = self.connections_dict[connection].time
                # Debug: Log chosen path and quality
                # print(f"Current Station: {traject_object.location}")
                # print(f"Next Station: {next_station}")
                # print(f"Connection: {connection}")
                # print(f"Path Quality: {best_quality}")
                # print(f"Time: {time}, total time {self.get_total_time() + float(time)}")


                traject_object.update(connection, next_station, time)
                self.connections_dict[connection].update_used()
            else:
                # print(f"[DEBUG] No valid path from {traject_object.location}. Traject finished.")

                traject_object.finished = True
        else:
            # print(f"[DEBUG] No valid connections from {traject_object.location}. Traject finished.")

            traject_object.finished = True

    # def initialize_traject(self, color_list_i):
    #     """
    #     Use Greedy's initialize_traject.
    #     """
    #     return super().initialize_traject(color_list_i)
    # def initialize_traject(self, color_list_i):
    #     """
    #     Initialize traject for GreedyLookahead using the TrajectAnalyzer.
    #     """
    #     self.finished = False
    #     ta = TrajectAnalyzer(self.stations_dict, self.connections_dict, self.traject_list, self.connections_set)
    #     start_location = ta.find_next_start_location()
    #     print(f"start station {start_location}")
    #
    #
    #     if not start_location:
    #         print(f"[DEBUG] Geen startstation beschikbaar voor traject {color_list_i}.")
    #         return None
    #
    #     traject_object = Traject2(start_location, self.color_list[color_list_i])
    #     self.traject_list.append(traject_object)
    #     return traject_object


    # def run(self):
    #     """
    #     Run the greedy lookahead algorithm.
    #     """
    #     for i in range(self.number_of_trajects):
    #         traject_object = self.initialize_traject(i)
    #
    #         while not traject_object.finished:
    #             self.movement(traject_object)



    # def get_next_connection(self, traject_object, lookahead = 2):
    #     """
    #     Find the best connection with the knowlegde of lookahead steps.
    #     """
    #     valid_connections = self.valid_connection_options(traject_object)
    #     if not valid_connections:
    #         return None, []
    #
    #     best_quality = float('-inf')
    #     best_connection = None
    #     best_route = []
    #
    #     for connection, time in valid_connections.items():
    #
    #         # make connection string on alphabetical order
    #         connection_combination = f"{sorted([traject_object.location, connection])[0]}_{sorted([traject_object.location, connection])[1]}"
    #
    #         # checks if the connection is already visted if so it will check next connection
    #         if connection_combination in traject_object.connection_history:
    #             continue
    #
    #         total_quality, route = self.simulate_lookahead(traject_object, connection, lookahead)
    #         # print(f"all routes {route}")
    #         used_connections = self.connections_dict[connection_combination].times_used
    #         next_connection_quality, p = self.calculate_quality()
    #         print(f"connection {connection}, quality {total_quality}")
    #
    #
    #         # If the connection has already been used it will give a penalty
    #         if used_connections > 0:
    #             total_quality -= 1000
    #
    #         if total_quality > best_quality:
    #             best_quality = total_quality+1000
    #             best_connection = connection
    #             print(f"best connection {connection}, quality {best_quality}")
    #
    #             # the best combination of stations
    #             best_route = route
    #             # print(f"chosen route {best_route}")
    #
    #     return best_connection, best_route
    #
    # def simulate_lookahead(self, traject_object, connection, lookahead_steps):
    #     total_quality = 0
    #     # a list for the possible route
    #     route = []
    #
    #     # make a copy to simulate a lookahead without effecting the original
    #     current_traject = copy.deepcopy(traject_object)
    #
    #     # move to connection
    #     self.movement(current_traject, connection)
    #
    #     # append first station in route
    #     route.append(connection)
    #
    #     connection_quality, p = self.calculate_quality()
    #     total_quality += connection_quality
    #
    #     for i in range(lookahead_steps):
    #         next_connection, best_route = self.get_next_connection(current_traject)
    #         if next_connection is None:
    #             break
    #
    #         next_connection_quality, p = self.calculate_quality()
    #         total_quality += next_connection_quality
    #         self.movement(current_traject, next_connection)
    #         route.append(next_connection)
    #
    #     return total_quality, route
    #
    #
    # def run(self):
    #     """
    #     Run the greedy lookahead algorithm.
    #     """
    #
    #
    #     for i in range(self.number_of_trajects):
    #         start_location = self.start_station()
    #         traject_object = Traject2(start_location, self.color_list[i])
    #         self.traject_list.append(traject_object)
    #
    #         while not traject_object.finished:
    #             best_station, best_route = self.get_next_connection(traject_object)
    #             if not best_station:
    #                 traject_object.finished = True
    #                 break
    #
    #             # uses only the stations with the best combination of quality
    #             for station in best_route:
    #                 self.movement(traject_object, station)
    #
    #                 # checks if traject is finished
    #                 if traject_object.finished:
    #                     break


        # self.initialize_trajects()
        #
        # for traject_object in self.traject_list:
        #     while not traject_object.finished:
        #         best_station, best_route = self.get_next_connection(traject_object)
        #         if not best_station:
        #             traject_object.finished = True
        #             break
        #
        #         # uses only the stations with the best combination of quality
        #         for station in best_route:
        #             self.movement(traject_object, station)
        #
        #             # checks if traject is finished
        #             if traject_object.finished:
        #                 break
