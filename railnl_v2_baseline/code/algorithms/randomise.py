import random

def random_select_next_station(valid_connections):
    """
    Randomly selects the next station from valid connection options.
    If no valid connections exist, returns None.
    """
    if not valid_connections:  # If no valid connections, return None
        return None
    else:
        return random.choice(list(valid_connections.keys()))


def random_start_station(list_of_stations):
    """
    Return random starting station from list of stations.
    """
    return random.choice(list(list_of_stations))
