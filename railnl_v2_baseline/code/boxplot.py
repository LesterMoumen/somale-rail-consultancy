
import matplotlib.pyplot as plt
from code.classes.train_table import Train_table

def create_box_plot(connections, locations, number_of_trajects, max_time, start_location_algorithm, select_next_station_algoritm, N=100, plot_name=None):
    #connections_file, locations_file, number_of_trajects, max_time, N=100, plot_name=None):

    best_quality = 0
    data = []
    for trajects in range(1, number_of_trajects+1):

        # Run the experiment N times to collect data
        traject_data = []
        for i in range(N):
            train_table_object = Train_table(connections, locations, trajects, max_time, start_location_algorithm, select_next_station_algoritm )
            train_table_object.create_table()
            quality = int(train_table_object.calculate_quality())
            traject_data.append(quality)

            if quality > best_quality:
                best_quality = quality
                best_train_table = train_table_object

        data.append(traject_data)


    # Make the plot
    plt.boxplot(data)
    plt.xlabel("Number of trajects")
    plt.ylabel("Quality score")
    plt.title(plot_name)
    plt.show()

    return best_train_table, best_quality
