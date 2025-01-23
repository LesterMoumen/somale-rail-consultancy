

class Traject2():
    """ Handles a single train route/traject.
    """
    def __init__(self, start_location, color):
        self.location = start_location # current station
        self.color = color # color of the traject
        self.connection_history = [] # list with connections visited
        self.traject_time = 0 # minutes traveled
        ##self.max_time = max_time # max time in minutes
        self.finished = False # initiate track as unfinished
        self.station_history = [start_location]

    def update(self, new_connection, new_station, new_time):
        self.location = new_station
        self.connection_history.append(new_connection)
        self.station_history.append(new_station)
        self.traject_time += int(new_time)
