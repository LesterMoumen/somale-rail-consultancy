import copy
import random
# from code.classes.train_table import Train_table
from code.algorithms.experiment import Experiment
from code.classes.traject2 import Traject2


class Greedy(Experiment):
    def start_station(self, list_of_stations):
        """ Return random starting station from list of stations.
        """
        start_station_ran = random.choice(list(list_of_stations))
        # print(f"start_Station {start_station_ran}")
        return start_station_ran

    def get_next_connection(self, traject_object):
        valid_connections = self.valid_connection_options(traject_object)
        if not valid_connections:
            return None

        best_quality = float('-inf')
        best_connection = None
        current_location = traject_object.location
        for connection, time in valid_connections.items():
            print(f"connection: {connection}")
            print(f"current_location; {traject_object.location}")
            print(f"connection_history: {traject_object.connection_history}")
            plakkend = current_location + "_" + connection
            print(f"plakkend: {plakkend}")
            for connections in traject_object.connection_history:
                connection1, connection2 = connections.split('_')
                # print(connection1, connection2)
                if (connection == connection1) or (connection == connection2):
                    continue

            next_connection_quality, p = self.calculate_quality()

            # print(f"{connection}, next_connection_quality: {next_connection_quality}")
            if next_connection_quality > best_quality:
                best_quality = next_connection_quality
                best_connection = connection
        # print(f"{best_connection} met k {best_quality}")

        return best_connection

    def run(self):
        self.initialize_trajects()
        for traject_object in self.traject_list:
            # print(f"start traject {traject_object}")
            while not traject_object.finished:
                next_station = self.get_next_connection(traject_object)
                if next_station is None:
                    # print(f"no vallid connections left")
                    traject_object.finished = True
                    break
                # print(f"moving to next station {next_station}")
                self.movement(traject_object, next_station)


    def movement(self, traject_object, next_station):
        """ To do: Move to experiment with (self, next_station)
        """
        if next_station is None:
            traject_object.finished = True

        else:
            connection = f"{sorted([traject_object.location, next_station])[0]}_{sorted([traject_object.location, next_station])[1]}"
            time = self.connections_dict[connection].time
            traject_object.update(connection, next_station, time)

            # Update times ued
            self.connections_dict[connection].update_used()



# class GreedyLookahead(Greedy):
