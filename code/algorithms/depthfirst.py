import copy
from code.classes.station import Station

class DepthFirstCounter:
    def __init__(self, stations, max_time):
        self.station_dict = stations
        self.max_time = max_time

    def count_all_possible_trajectories(self):
        """
        Counts all possible trajectories for the entire map within the time constraint.
        """
        total_trajectories = 0

        # Loop over all stations as starting points
        for station in self.station_dict.keys():
            total_trajectories += self.count_possible_trajectories(station)

        return total_trajectories

    def count_possible_trajectories(self, start_station):
        """
        Counts all possible trajectories starting from a given station within the time constraint using a stack.
        """
        stack = [(start_station, self.max_time)]  # Stack to hold (current station, remaining time)
        trajectories = 0

        while stack:
            current_station, remaining_time = stack.pop()

            # Count the current trajectory
            trajectories += 1

            # Add neighbors to the stack if they can be reached within the remaining time
            for neighbor, travel_time in self.station_dict[current_station].connections.items():
                travel_time = int(travel_time)
                if travel_time <= remaining_time:
                    stack.append((neighbor, remaining_time - travel_time))

        return trajectories
