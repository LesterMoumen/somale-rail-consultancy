
from . import helper_functions as helper

class Connection():
    def __init__(self, station1, station2, time):
            """ Connections is a csv file that has all the connections with connection times
            stations is a dict that has {station_name : station_object}, stattion_object
            has values such as .connection, .x, .y, etc.
            """
            self.station1 = station1
            self.station2 = station2
            self.time = time
            self.times_used = 0

    def update_used(self):
        self.times_used += 1
