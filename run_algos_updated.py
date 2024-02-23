import matplotlib.pyplot as plt
import numpy as np
from TSP_Common import read_lower_triangular_matrix, calculate_distance, two_opt_updated, create_full_matrix, print_matrix

from TSP_NN import nearest_neighbor_tsp
from TSP_H import generate_random_tour
from TSP_HPrime import prim_mst, create_tour_from_spanning_tree2
import sys
import time

MAX_CITIES = 3000

GRAPH_FILES = [
    "Graphs/470_Graphs/g100.graph",
    "Graphs/470_Graphs/g200.graph",
    "Graphs/470_Graphs/g300.graph",
    "Graphs/470_Graphs/g400.graph",
    "Graphs/470_Graphs/g500.graph",
    "Graphs/470_Graphs/g600.graph",
    "Graphs/470_Graphs/g700.graph",
    "Graphs/470_Graphs/g800.graph",
    "Graphs/470_Graphs/g900.graph",
    "Graphs/470_Graphs/g1000.graph",
]

def set_up_matrix(file_path):
    lower_triangular_matrix = read_lower_triangular_matrix(file_path)
    full_matrix = create_full_matrix(lower_triangular_matrix)

    return (full_matrix,lower_triangular_matrix)

def nearest_neighbor(lower_triangular_matrix):
    _,new_distance = nearest_neighbor_tsp(lower_triangular_matrix)

    return new_distance

def two_opt_fun(lower_triangular_matrix, full_matrix):
    tour = generate_random_tour(lower_triangular_matrix)

    optimized_tour = two_opt_updated(tour, full_matrix)
    optimized_distance = calculate_distance(optimized_tour,lower_triangular_matrix)

    return optimized_distance

def two_opt_mst(lower_triangular_matrix, full_matrix):
    minimum_spanning_tree = prim_mst(lower_triangular_matrix)

    tour = create_tour_from_spanning_tree2(minimum_spanning_tree, len(lower_triangular_matrix))

    optimized_tour = two_opt_updated(tour, full_matrix) # O(N^2)
    optimized_distance = calculate_distance(optimized_tour,lower_triangular_matrix) # O(N)

    return optimized_distance

def run_against_my_graphs(num_cities, nn, two_opt, two_mst): #pass in arrays?
    # num_cities = 1500
    for i in range(500, num_cities, 500): # O(N/500)
        fileName = f"Graphs\MyGraphs\g{i}M.txt"
        fullm, lowm = set_up_matrix(fileName)

        print(f"\nStarting Size: {i}")

        nn.append( nearest_neighbor(lowm))
        # print("Fin NN")

        two_opt.append(two_opt_fun(lowm, fullm))
        # print("Fin 2opt H")

        two_mst.append(two_opt_mst(lowm, fullm))
        # print("Fin 2opt HPrime\n")
# end
        
def run_against_470_graphs(nn, two_opt, two_mst): #pass in arrays?
    # num_cities = 1500
    for fileN in GRAPH_FILES: # O(N/500)
        fullm, lowm = set_up_matrix(fileN)

        print(f"Starting Size: {fileN}\n")

        nn.append( nearest_neighbor(lowm))
        # print("Fin NN")

        two_opt.append(two_opt_fun(lowm, fullm))
        # print("Fin 2opt H")

        two_mst.append(two_opt_mst(lowm, fullm))
        # print("Fin 2opt HPrime\n")
# end

def run_algos_on_file(fileName): #pass in arrays?

    fullm, lowm = set_up_matrix(fileName)

    print(f"Starting With File: {fileName}\n")

    start_time = time.time()
    nn = nearest_neighbor(lowm)
    end_time = time.time()
    print(f"Fin NN in {end_time - start_time: .6f} s")

    start_time = time.time()
    two_opt = two_opt_fun(lowm, fullm)
    end_time = time.time()
    print(f"Fin 2opt in {end_time - start_time: .6f} s")

    start_time = time.time()
    two_mst = two_opt_mst(lowm, fullm)
    end_time = time.time()
    print(f"Fin 2opt HPrime in {end_time - start_time:.6f}s\n")

    return (nn, two_opt, two_mst)
# end

def run_my_graphs_avg(num_cities, num_runs, nn, two_opt, two_mst):
    for run in range(num_runs):
        print(f"Run {run + 1}/{num_runs}\n")
        
        nn_run = []
        two_opt_run = []
        two_mst_run = []

        run_against_my_graphs(num_cities, nn_run, two_opt_run, two_mst_run) #pass in arrays?
    
        nn.append(nn_run)
        two_opt.append(two_opt_run)
        two_mst.append(two_mst_run) #should be multiples of original run

    # Calculate averages
    nn_avg = np.mean(np.array(nn), axis=0)
    two_opt_avg = np.mean(np.array(two_opt), axis=0)
    two_mst_avg = np.mean(np.array(two_mst), axis=0)

    return nn_avg, two_opt_avg, two_mst_avg
# end run all

def run_against_470_graphs_n_times(num_runs, nn, two_opt, two_mst):
    for run in range(num_runs):
        print(f"Run {run + 1}/{num_runs}\n")
        
        nn_run = []
        two_opt_run = []
        two_mst_run = []

        run_against_470_graphs(nn_run, two_opt_run, two_mst_run) #pass in arrays?

        nn.append(nn_run)
        two_opt.append(two_opt_run)
        two_mst.append(two_mst_run)

    # Calculate averages
    nn_avg = np.mean(np.array(nn), axis=0)
    two_opt_avg = np.mean(np.array(two_opt), axis=0)
    two_mst_avg = np.mean(np.array(two_mst), axis=0)

    return nn_avg, two_opt_avg, two_mst_avg
# end run all

def print_distances(array, name): # O(N)
    print(f"{name}: ")
    for dist in array:
        print(f"{dist} ")
# end print matrix

def print_and_plot_distances(algo_distances, graph_sizes, algo_labels, title =
                              "TSP Algorithm Performance", ylabel='Distance of Route'):
    # Print distances
    print("TSP Algorithm Performance: ")
    for dist in algo_distances:
        print(f"{dist} ")

    # Plotting
    # graph_sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    
    for distances, label in zip(algo_distances, algo_labels):
        plt.plot(graph_sizes, distances, label=label)

    plt.xlabel("Graph Size")
    plt.ylabel(ylabel)
    plt.legend()
    plt.title(title)
    plt.show()
# end print and plot
    
if __name__ == "__main__":
    
    # For accumulated graph
    NUM_RUNS = 2

    if len(sys.argv) > 1:
        file_choice = str(sys.argv[1])
        nn, two_opt, two_mst = run_algos_on_file(file_choice)
        print("Results:")
        print(f" NN: {nn}\n 2-Opt: {two_opt}\n 2-Opt + MST: {two_mst}")
        exit()

    else:
        print("Choose a Test to run:")
        print("1. Personal Graphs 1 Run")
        print("2. 470 Graphs 1 Run")
        print(f"3. Personal Graph Accumulated ({NUM_RUNS} Time(s)  Cities - ({MAX_CITIES})")
        print(f"4. 470 Graph Accumulated ({NUM_RUNS} Time(s))")
        print("5. To exit")

        algo_choice = int(input("\nEnter the algorithm number: "))

    if algo_choice not in [1, 2, 3, 4, 5]:
        print("Invalid algorithm choice. Please choose 1, 2, 3, 4, or 5.")
        sys.exit(1)
    elif algo_choice == 5:
        print("\nExiting Now!")
        sys.exit(1)
    
    nn_distances = []
    two_opt_distances = []
    two_opt_mst_distances = []
    
    algo_labels = ["NN", "2-Opt","Heuristic 2-Opt + MST" ]

    # Based on the algorithm choice, call the appropriate function
    if algo_choice == 1:
        print("\nOption: \n")
        print(f"Enter Max_Cities up to 7k - curr({MAX_CITIES}):")
        print(f"Enter 'N' for defaults. \n")
        user_cities = int(input("\nEnter # Cities or N: "))

        if user_cities != 'N' or user_cities != 'n':
            MAX_CITIES = user_cities

        graph_sizes = list(range(500, MAX_CITIES, 500))

        run_against_my_graphs(MAX_CITIES, nn_distances, two_opt_distances, two_opt_mst_distances)

        algo_distances = [nn_distances, two_opt_distances, two_opt_mst_distances]
        title = f"TSP - Personal Graph - {MAX_CITIES} Cities(s) - {(MAX_CITIES / 500)-1} Graph(s)"

        print_and_plot_distances(algo_distances, graph_sizes, algo_labels, title)

    elif algo_choice == 2:
        graph_sizes = [100,200,300,400,500,600,700,800,900,1000]

        run_against_470_graphs(nn_distances, two_opt_distances, two_opt_mst_distances)

        algo_distances = [nn_distances, two_opt_distances, two_opt_mst_distances]
        title = f"TSP - 470 Graphs - {len(GRAPH_FILES)} Graph(s)"

        print_and_plot_distances(algo_distances,
                                  graph_sizes, algo_labels, title)

    elif algo_choice == 3:
        print("\nOptions: \n")
        print(f"Enter Max_Cities up to 7k - curr({MAX_CITIES}):")
        print(f"Enter number of runs. Reccomend 1 for Cities over 4k - curr({NUM_RUNS}):")
        print(f"Enter 'N' for defaults. \n")
        user_cities = int(input("Enter # Cities or N: "))

        if user_cities != 'N' or user_cities != 'n':
            MAX_CITIES = user_cities
            user_runs = int(input("\nEnter # Runs: "))
            NUM_RUNS = user_runs

        graph_sizes = list(range(500, MAX_CITIES, 500))

        nn_avg, two_opt_avg, two_opt_mst_avg = run_my_graphs_avg(
            MAX_CITIES, NUM_RUNS, nn_distances, two_opt_distances, two_opt_mst_distances)
        
        algo_distances = [nn_avg, two_opt_avg, two_opt_mst_avg]

        title = f"TSP - Personal Graph Accumulated - {NUM_RUNS} Run(s)"

        print_and_plot_distances(algo_distances, graph_sizes, algo_labels,title, 
                                 "Average Distance of Route")
        
    elif algo_choice == 4:
        graph_sizes = [100,200,300,400,500,600,700,800,900,1000]

        nn_avg, two_opt_avg, two_opt_mst_avg = run_against_470_graphs_n_times(
            NUM_RUNS, nn_distances, two_opt_distances, two_opt_mst_distances)
        
        algo_distances = [nn_avg, two_opt_avg, two_opt_mst_avg]

        title = f"TSP Algorithm Performance - 470 Graph Accumulated - {NUM_RUNS} Run(s)"

        print_and_plot_distances(algo_distances, graph_sizes, algo_labels, title, 
                                 "Average Distance of Route")
    # end if
# end main
