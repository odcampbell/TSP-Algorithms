import itertools
import time
import random

def generate_random_distances(n):
    distances = [[0] * n for _ in range(n)] # N by n Zeros?

    for i in range(n):
        for j in range(i + 1, n):
            # Generate random distance (integer between 1 and 100)
            distances[i][j] = distances[j][i] = random.randint(1, 100)

    return distances

def calculate_distance(route, distances):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distances[route[i]][route[i + 1]]
    # Return to the starting city
    total_distance += distances[route[-1]][route[0]]
    return total_distance

def brute_force_tsp(distances):
    n = len(distances)
    cities = list(range(n))
    min_distance = float('inf')
    optimal_route = []

    # Generate all possible permutations of cities
    for route_permutation in itertools.permutations(cities):
        current_distance = calculate_distance(route_permutation, distances)
        # Update minimum distance and optimal route if a shorter route is found
        if current_distance < min_distance:
            min_distance = current_distance
            optimal_route = list(route_permutation)

    return optimal_route, min_distance

# number of cities (N)
N = 10

# Hardcoded full matrix example for 10 cities
example_distances = [[0, 83, 25, 52, 27, 56, 85, 83, 86, 98], [83, 0, 37, 73, 79, 54, 21, 74, 75, 14], [25, 37, 0, 56, 100, 62, 14, 58, 43, 100], [52, 73, 56, 0, 65, 11, 54, 30, 77, 19], [27, 79, 100, 65, 0, 42, 63, 79, 62, 76], [56, 54, 62, 11, 42, 0, 85, 21, 81, 67], [85, 21, 14, 54, 63, 85, 0, 55, 23, 1], [83, 74, 58, 30, 79, 21, 55, 0, 6, 49], [86, 75, 43, 77, 62, 81, 23, 6, 0, 64], [98, 14, 100, 19, 76, 67, 1, 49, 64, 0]]

# Optimal Route: [0, 2, 1, 9, 6, 8, 7, 3, 5, 4]
# Optimal Distance: 216 units
print(example_distances)

# Generate random distances for N cities
# example_distances = generate_random_distances(N)

start_time = time.time()
optimal_route, min_distance = brute_force_tsp(example_distances)
end_time = time.time()

# Output the result and time taken
print("Optimal Route:", optimal_route)
print("Optimal Distance:", min_distance, "units")
print("Time Taken:", end_time - start_time, "seconds")

# My brute force took 4 seconds at 10 cities, but over a minute at 11 (71 seconds)
# Puts my constant around 71/ (1.8 x 10^-6)
# N=12 would take about 15 min, N = 13 would take around 15 hours..