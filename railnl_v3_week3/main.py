# Baseline version

#from code.classes.train_table import Train_table
#from code.classes.trajectanalyzer import *
#from code.boxplot import create_box_plot
#from code.algorithms.depthfirst import DepthFirstCounter
#from code.classes.station import Station
from code.algorithms.experiment import Experiment
from code.algorithms.randomise import Randomise
from code.algorithms.run_experiments import RunExperiments

# Data files
locations_holland = "data/StationsHolland_locaties.csv"
connections_holland = "data/ConnectiesHolland.csv"
locations_national = "data/StationsNationaal_locaties.csv"
connections_national = "data/ConnectiesNationaal.csv"

# Parameters
connections_file = connections_holland
locations_file = locations_holland
max_number_of_trajects = 7
max_time = 120

if __name__ == "__main__":
    # ____Run single experiment____
    # e.g. with randomise and 2 trajects
    number_of_trajects = 4
    randomised_experiment = Randomise(connections_file, locations_file, number_of_trajects, max_time)
    randomised_experiment.run()
    # Print output in terminal
    randomised_experiment.print_output()

    # ____Run multiple experiments___
    # e.g. with randomise algorithms
    algorithm = Randomise
    number_of_experiments = 100
    r = RunExperiments(connections_file, locations_file, max_number_of_trajects, max_time, number_of_experiments, algorithm_type = algorithm)
    r.run()
    r.create_boxplot()
