from code.classes.experiment import Experiment

class DepthFirstCounter(Experiment):
    def __init__(self, connections_file, locations_file, number_of_trajects, max_time):
        # Initialize the parent class
        super().__init__(connections_file, locations_file, number_of_trajects, max_time)

        # Add attributes specific to DepthFirstCounter
        self.visited_trajectories = set()

    def count_all_possible_trajectories(self):
        """
        Counts all possible unique trajectories for the entire map within the time constraint.
        """
        total_trajectories = 0

        # Loop over all stations as starting points
        for station in self.stations_dict.keys():
            total_trajectories += self.count_possible_trajectories(station)

        return total_trajectories

    def count_possible_trajectories(self, start_station):
        """
        Counts all possible unique trajectories starting from a given station within the time constraint using a stack.
        """
        stack = [(start_station, self.max_time, [])]  # Stack to hold (current station, remaining time, current path)
        trajectories = 0

        while stack:
            current_station, remaining_time, current_path = stack.pop()

            # Explore neighbors
            for neighbor, travel_time in self.stations_dict[current_station].connections.items():
                travel_time = int(travel_time)

                if travel_time <= remaining_time:
                    # Create the next connection and normalize it as a tuple
                    connection = tuple(sorted([current_station, neighbor]))
                    new_path = current_path + [connection]

                    # Normalize the entire trajectory path
                    normalized_path = tuple(sorted(new_path))

                    if normalized_path not in self.visited_trajectories:
                        # Mark trajectory as visited
                        self.visited_trajectories.add(normalized_path)
                        # Count this unique trajectory
                        trajectories += 1

                        # Add the neighbor to the stack for further exploration
                        stack.append((neighbor, remaining_time - travel_time, new_path))

            if len(self.visited_trajectories) % 100000 == 0:
                print(f"Checked {len(self.visited_trajectories)} unique paths so far...")

        return trajectories
