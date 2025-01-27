import copy
import random
from code.algorithms.experiment import Experiment
from code.classes.traject2 import Traject2


class Greedy(Experiment):
    def start_station(self, list_of_stations):
        """
        Return random starting station from list of stations.
        """
        start_station_random = random.choice(list(list_of_stations))
        return start_station_random

    def get_next_connection(self, traject_object):
        """
        Returns the next connection which has the highest quality.
        - It avoids connections which already has been visited
        """
        valid_connections = self.valid_connection_options(traject_object)
        if not valid_connections:
            return None #if there are no connection options

        best_quality = float('-inf')
        best_connection = None
        for connection, time in valid_connections.items():

            # make connection string on alphabetical order
            connection_combination = f"{sorted([traject_object.location, connection])[0]}_{sorted([traject_object.location, connection])[1]}"
            # checks if the connection is already visted if so it will check next connection
            if connection_combination in traject_object.connection_history:
                continue

            
            used_connections = self.connections_dict[connection_combination].times_used
            next_connection_quality, p = self.calculate_quality()

            # If the connection has already been used it will give a penalty
            if used_connections > 0:
                next_connection_quality -= 1000

            if next_connection_quality > best_quality:
                best_quality = next_connection_quality
                best_connection = connection
                print(f"best connection {connection}, quality {best_quality}")
                # print(best_connection)
        return best_connection

    def run(self):
        """
        Run the greedy algorithm.
        """
        self.initialize_trajects()
        for traject_object in self.traject_list:
            while not traject_object.finished:
                best_station = self.get_next_connection(traject_object)
                if best_station is None:
                    traject_object.finished = True
                    break
                self.movement(traject_object, best_station)


    def movement(self, traject_object, next_station):
        """
        Movement of traject_object to next station
        """
        if next_station is None:
            traject_object.finished = True

        else:

            # make connection string on alphabetical order
            connection = f"{sorted([traject_object.location, next_station])[0]}_{sorted([traject_object.location, next_station])[1]}"
            time = self.connections_dict[connection].time
            traject_object.update(connection, next_station, time)

            # Update the connection as used
            self.connections_dict[connection].update_used()



class GreedyLookahead(Greedy):
    def get_next_connection(self, traject_object, lookahead = 3):
        """
        Find the best connection with the knowlegde of lookahead steps.
        """
        valid_connections = self.valid_connection_options(traject_object)
        if not valid_connections:
            return None, []

        best_quality = float('-inf')
        best_connection = None
        best_route = []

        for connection, time in valid_connections.items():

            # make connection string on alphabetical order
            connection_combination = f"{sorted([traject_object.location, connection])[0]}_{sorted([traject_object.location, connection])[1]}"

            # checks if the connection is already visted if so it will check next connection
            if connection_combination in traject_object.connection_history:
                continue

            total_quality, route = self.simulate_lookahead(traject_object, connection, lookahead)
            # print(f"all routes {route}")
            used_connections = self.connections_dict[connection_combination].times_used
            next_connection_quality, p = self.calculate_quality()
            print(f"connection {connection}, quality {total_quality}")


            # If the connection has already been used it will give a penalty
            if used_connections > 0:
                total_quality -= 1000

            if total_quality > best_quality:
                best_quality = total_quality+1000
                best_connection = connection
                print(f"best connection {connection}, quality {best_quality}")

                # the best combination of stations
                best_route = route
                # print(f"chosen route {best_route}")

        return best_connection, best_route

    def simulate_lookahead(self, traject_object, connection, lookahead_steps):
        total_quality = 0
        # a list for the possible route
        route = []

        # make a copy to simulate a lookahead without effecting the original
        current_traject = copy.deepcopy(traject_object)

        # move to connection
        self.movement(current_traject, connection)

        # append first station in route
        route.append(connection)

        connection_quality, p = self.calculate_quality()
        total_quality += connection_quality

        for i in range(lookahead_steps):
            next_connection, best_route = self.get_next_connection(current_traject)
            if next_connection is None:
                break

            next_connection_quality, p = self.calculate_quality()
            total_quality += next_connection_quality
            self.movement(current_traject, next_connection)
            route.append(next_connection)

        return total_quality, route


    def run(self):
        """
        Run the greedy lookahead algorithm.
        """
        self.initialize_trajects()

        for traject_object in self.traject_list:
            while not traject_object.finished:
                best_station, best_route = self.get_next_connection(traject_object)
                if not best_station:
                    traject_object.finished = True
                    break

                # uses only the stations with the best combination of quality
                for station in best_route:
                    self.movement(traject_object, station)

                    # checks if traject is finished
                    if traject_object.finished:
                        break
