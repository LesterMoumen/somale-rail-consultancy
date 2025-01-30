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
    def __init__(self, train_table, mutate_trajects_number, mutate_tracks_number, temperature=1200, alpha=0.98):
        # Use the init of the HillClimber class
        super().__init__(train_table, mutate_trajects_number, mutate_tracks_number)

        # Starting temperature and current temperature
        self.T0 = temperature
        self.T = temperature
        self.alpha = alpha

        self.no_improvement_counter = 0
        self.no_improvement_threshold = 2000

        self.total_delta = 0
        self.highest_delta = 0
        self.lowest_delta = 100


    def reheat(self):
        print('Reheating the model.')
        return 0.15 * self.T0


    def normalize_delta(self, delta, current_score):
        """
        Normalizes the delta by dividing it by the current score.
        This ensures that the delta is scale-invariant.
        """
        if current_score == 0:
            return delta  # Avoid division by zero
        return delta / current_score


    def update_temperature(self, iteration):
        """
        This function implements a *linear* cooling scheme.
        Temperature will become zero after all iterations passed to the run()
        method have passed.
        """
        # #Linear
        # self.T = self.T - (self.T0 / self.iterations)

        # Exponential would look like this:
        # self.T = self.T * self.alpha
        self.T = self.T * self.alpha

        # Prevent the temperature from getting too small
        if self.T < 0.001:
            self.T = 0.1  # Set a minimum temperature value

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

        # # Normalized delta
        #delta = self.normalize_delta(delta, old_value)

        print(f"Old Value: {old_value}, New Value: {new_value}, Temperature: {self.T}, Raw Delta: {old_value - new_value}")
        print(f" Normalized Delta: {delta}")

        # Count delta to get average for 'normalizing' delta
        self.total_delta += delta
        if delta > self.highest_delta:
            self.highest_delta = delta

        # Increase counter if model is not converging
        if delta > 0:
            self.no_improvement_counter += 1

        probability = math.exp(-delta / self.T)

        # Pull a random number between 0 and 1 and check if new table is accepted
        if random.random() < probability:
            self.train_table = new_table
            self.value = new_value

        # Update the temperature
        self.update_temperature(iteration)


    def run(self, iterations, verbose=False):
        """
        Runs the HillClimber algorithm for the specified number of iterations.
        """

        for iteration in range(iterations):
            print(f'Iteration {iteration}/{iterations}, current value: {self.value}') if verbose else None

            # Reheat
            # if self.no_improvement_counter >= self.no_improvement_threshold:
            #   self.reheat()
            #   self.no_improvement_counter = 0


            # Generate a neighboring solution
            new_table = copy.deepcopy(self.train_table)
            # Evaluate the neighboring solution
            self.mutate_table(new_table)
            # Evalute new train table
            self.check_solution(new_table, iteration)

        # After all iterations, print the final temperature
        print(f"Final temperature: {self.T:.4f}")
        print(f"average delta: {self.total_delta/iterations}")
        print(f"highest delta: {self.highest_delta}")
