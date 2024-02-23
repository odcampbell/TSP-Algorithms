import sys
import time
# import numpy as np
import random
from TSP_Common import read_lower_triangular_matrix, calculate_distance, two_opt, find_largest_edges_per_node, two_opt_updated, create_full_matrix, print_matrix


def generate_random_tour(lower_triangle_matrix):
    num_cities = len(lower_triangle_matrix)
    cities = list(range(num_cities))

    # Start with a random city
    current_city = 0
    tour = [current_city]
    cities.remove(current_city)

    # Generate the rest of the tour randomly
    while cities:
        next_city = random.choice(cities)
        tour.append(next_city)
        cities.remove(next_city)

    # Return to the starting city to complete the tour
    tour.append(tour[0])

    return tour #_edges

def generate_random_tour2(lower_triangle_matrix, excluded_edges=[]):
    num_cities = len(lower_triangle_matrix)
    cities = list(range(num_cities))

    # Start with a random city
    current_city = 0
    tour = [current_city]
    cities.remove(current_city)

    # Generate the rest of the tour randomly
    while cities:
        next_city = random.choice(cities)
        # Check if the edge is not in the excluded_edges list
        if (current_city, next_city) not in excluded_edges and (next_city, current_city) not in excluded_edges:
            tour.append(next_city)
            cities.remove(next_city)

            # Check if only one city is left, then add it to complete the tour
            if len(cities) == 1:
                tour.append(cities[0])
                break

    return tour

# Random performed better, sometiems a longer edge can make for a shorter tour
def comp_edges(lower_triangular_matrix):
    # run two opt add up distances, compare average
    tries = 5
    distance1 = 0
    distance2 = 0
    edges = find_largest_edges_per_node(lower_triangular_matrix)
    full_matrix = create_full_matrix(lower_triangular_matrix)

    for _ in range (tries):
        tour2 = generate_random_tour2(lower_triangular_matrix, edges)
        tour1 = generate_random_tour(lower_triangular_matrix) #long

        with open("comp1.txt", 'w') as output_file:
            for city in tour1:
                output_file.write(str(city))
        
        with open("comp2.txt", 'w') as output_file:
            for city in tour2:
                output_file.write(str(city))

        # _, optimized_distance1= two_opt(tour1, lower_triangular_matrix)
        optimized_tour1= two_opt_updated(tour1, full_matrix)
        optimized_distance1 = calculate_distance(optimized_tour1,lower_triangular_matrix)

        # _, optimized_distance2= two_opt(tour2, lower_triangular_matrix)
        optimized_tour2= two_opt_updated(tour2, full_matrix)
        optimized_distance2 = calculate_distance(optimized_tour2,lower_triangular_matrix)

        distance1 += optimized_distance1    
        distance2 += optimized_distance2    
    
    if(distance1 > distance2):
        print(f"LONG edges is better: Tour1 {distance1} , Tour2 {distance2}")
    else:
        print(f"LONG edges is worse: Tour1 {distance1} , Tour2 {distance2}")
# end comp two opt

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py file_path")
        sys.exit(1)

    file_path = sys.argv[1]

    lower_triangular_matrix = read_lower_triangular_matrix(file_path)
    # comp_edges(lower_triangular_matrix)
    full_matrix = create_full_matrix(lower_triangular_matrix)

    tour = generate_random_tour(lower_triangular_matrix)

    initial_distance = calculate_distance(tour, lower_triangular_matrix)

    output_file_name = "TSP_Output\TSP_H_Out.txt"
    with open(output_file_name, 'a') as output_file:
        output_file.write(f"\n\n---- TSP Heuristic Output ---- ")
        output_file.write(f"\nNumber of Cities:  {len(lower_triangular_matrix)}")
        output_file.write(f"\nInitial Distance::  {initial_distance}")
        # output_file.write(f"\n\nRandomGen_Initial_Tour:  {tour}")

    # optimize
    start_time = time.time()
    optimized_tour = two_opt_updated(tour, full_matrix)
    # optimized_tour = two_opt_updated(tour, full_matrix)
    elapsed_time = time.time() - start_time
    optimized_distance = calculate_distance(optimized_tour,lower_triangular_matrix)

    # Output the result
    with open(output_file_name, 'a') as output_file:
        output_file.write(f"\nOptimized Distance::  {optimized_distance}")
        output_file.write(f"\nExecution Time:  {elapsed_time} seconds")
        # output_file.write(f"\n\nOptimized Tour:  {optimized_tour}")

    print("Execution Time: ", elapsed_time, "seconds")
    print("Optimized Distance:", optimized_distance)
    

