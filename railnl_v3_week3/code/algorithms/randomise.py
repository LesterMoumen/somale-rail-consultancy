import random
from code.algorithms.experiment import Experiment
from code.classes.traject2 import Traject2

class Randomise(Experiment):
    """ This class handles the instance of an experiment with a random algorithm.
    The class inherits from the Experiment class, and adds the start_station and
    select_next_station function. Both functions do this randomly.
    """
    def start_station(self, list_of_stations):
        """ Return random starting station from list of stations.
        """
        return random.choice(list(list_of_stations))


    def select_next_station(self, valid_connections):
        """ Randomly selects the next station from valid connection options.
        If no valid connections exist, returns None.
        """
        if not valid_connections:
            return None
        else:
            return random.choice(list(valid_connections.keys()))
