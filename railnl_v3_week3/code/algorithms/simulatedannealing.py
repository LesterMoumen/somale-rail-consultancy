import random
import math
import copy

from code.algorithms.hillclimber import HillClimber


class SimulatedAnnealing(HillClimber):
    """
    The SimulatedAnnealing class that changes a random node in the graph to a random valid value.
    Each improvement or equivalent solution is kept for the next iteration.
    Also sometimes accepts solutions that are worse, depending on the current temperature.

    Most of the functions are similar to those of the HillClimber class, which is why
    we use that as a parent class.
    """
    def __init__(self, train_table, temperature=1200):
        # Use the init of the Hillclimber class
        super().__init__(train_table)

        # Starting temperature and current temperature
        self.T0 = temperature
        self.T = temperature

        self.no_improvement_counter = 0
        self.no_improvement_threshold = 2000

        self.total_delta = 0
        self.highest_delta = 0
        self.lowest_delta = 100

    def update_temperature(self, iteration):
        """
        This function implements a *linear* cooling scheme.
        Temperature will become zero after all iterations passed to the run()
        method have passed.
        """
        # #Linear
        # self.T = self.T - (self.T0 / self.iterations)

        # Exponential would look like this:
        alpha = 0.9995
        # self.T = self.T * alpha
        self.T = self.T * alpha

        # Prevent the temperature from getting too small
        if self.T < 0.001:
            self.T = 0.001  # Set a minimum temperature value

    def check_solution(self, new_table, iteration):
        """
        Checks and accepts better solutions than the current solution.
        Also sometimes accepts solutions that are worse, depending on the current
        temperature.
        """
        new_value = new_table.calculate_quality()[0]
        old_value = self.value

        # Calculate the probability of accepting this new graph
        delta = old_value - new_value
        print(f"Old Value: {old_value}, New Value: {new_value}, Delta: {delta}, Temperature: {self.T}")

        # Count delta to get average for 'normalizing' delta
        self.total_delta += delta
        if delta > self.highest_delta:
            self.highest_delta = delta

        # Increase counter if delta is above threshold
        if delta > 0:
            self.no_improvement_counter += 1

        probability = math.exp(-delta / self.T)

        # Pull a random number between 0 and 1 and see if we accept the graph!
        if random.random() < probability:
            self.train_table = new_table
            self.value = new_value

        # Update the temperature
        self.update_temperature(iteration)


    def run(self, iterations, verbose=False, mutate_trajects_number=1, mutate_tracks_number=3):
        """
        Runs the HillClimber algorithm for the specified number of iterations.
        """

        for iteration in range(iterations):
            print(f'Iteration {iteration}/{iterations}, current value: {self.value}') if verbose else None

            # Reheat
            # if self.no_improvement_counter >= self.no_improvement_threshold:
            #     self.T = 0.15 * self.T0
            #     self.no_improvement_counter = 0
            #     print('Reheating the model.')

            # Generate a neighboring solution
            new_table = copy.deepcopy(self.train_table)

            # Evaluate the neighboring solution
            self.mutate_table(new_table, number_of_trajects=mutate_trajects_number, number_of_tracks=mutate_tracks_number)
            # Evalute new train table
            self.check_solution(new_table, iteration)

        # After all iterations, print the final temperature
        print(f"Final temperature: {self.T:.4f}")
        print(f"average delta: {self.total_delta/iterations}")
        print(f"highest delta: {self.highest_delta}")
