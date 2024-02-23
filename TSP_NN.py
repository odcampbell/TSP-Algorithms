import sys
import time
from TSP_Common import read_lower_triangular_matrix

def nearest_neighbor_tsp(lower_triangle_matrix):
    num_cities = len(lower_triangle_matrix)
    
    # Start from the first city
    current_city = 0
    tour = [current_city]
    unvisited_cities = set(range(1, num_cities))
    total_distance = 0

    while unvisited_cities:
        # Find the nearest unvisited city
        nearest_city = min(unvisited_cities, key=lambda city: lower_triangle_matrix[max(city, current_city)][min(city, current_city)])
        
        # Add the nearest city to the tour
        tour.append(nearest_city)
        unvisited_cities.remove(nearest_city)
        
        # Update total distance
        total_distance += lower_triangle_matrix[max(nearest_city, current_city)][min(nearest_city, current_city)]
        
        # Move to the nearest city
        current_city = nearest_city

    # Return to the starting city to complete the tour
    tour.append(tour[0])
    total_distance += lower_triangle_matrix[current_city][tour[0]]

    return tour, total_distance
#end NN

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py file_path")
        sys.exit(1)

    file_path = sys.argv[1]
    lower_triangular_matrix = read_lower_triangular_matrix(file_path)

    # # Print the matrix
    # for row in lower_triangular_matrix:
    #     print(row)

    start_time = time.time()

    # Obtain the nearest neighbor tour
    tour,new_distance = nearest_neighbor_tsp(lower_triangular_matrix)
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Output the result
    output_file_name = "TSP_Output\TSP_NN_Out.txt"
    with open(output_file_name, 'a') as output_file:
        output_file.write(f"\n\n---- TSP NN Output ---- ")
        output_file.write(f"\nNumber of Cities:  {len(lower_triangular_matrix)}")
        output_file.write(f"\nOptimized Distance:  {new_distance}")
        output_file.write(f"\nElapsed Time:  {elapsed_time}seconds")
        # output_file.write(f"\n\nOptimized Tour:  {tour}")


    # print("Nearest Neighbor Tour:", tour)
    print("Distance:", new_distance)
    print("Elapsed Time:", elapsed_time, "seconds")

