import sys
import heapq
import time
from TSP_Common import calculate_distance, read_lower_triangular_matrix, two_opt_updated, create_full_matrix, two_opt


GRAPH_FILES = [
    "Graphs/g100.graph.txt",
    "Graphs/g200.graph.txt",
    "Graphs/g300.graph.txt",
    "Graphs/g400.graph.txt",
    "Graphs/g500.graph.txt",
    "Graphs/g600.graph.txt",
    "Graphs/g700.graph.txt",
    "Graphs/g800.graph.txt",
    "Graphs/g900.graph.txt",
    "Graphs/g1000.graph.txt",
]

def find_largest_edges_per_node(lower_triangle_matrix):
    largest_edges_per_node = []

    for i, row in enumerate(lower_triangle_matrix):
        # Exclude the diagonal elements and the current node
        non_zero_values = [value for j, value in enumerate(row[:i]) if value != 0]

        if non_zero_values:
            max_edge = max(non_zero_values)
            largest_edges_per_node.append((i, row.index(max_edge), max_edge))

    return largest_edges_per_node
# end find_largest_edges_per_node

def prim_mst(lower_triangle_matrix):
    num_cities = len(lower_triangle_matrix)
    visited = [False] * num_cities
    edges = []

    # Start from the first city
    start_city = 0
    visited[start_city] = True

    # Initialize the priority queue with edges from the starting city
    for city in range(1, num_cities):
        heapq.heappush(edges, (lower_triangle_matrix[city][start_city], start_city, city))

    mst_edges = []

    while edges:
        weight, from_city, to_city = heapq.heappop(edges)

        if not visited[to_city]:
            mst_edges.append((from_city, to_city, weight))
            visited[to_city] = True

            # Add edges from the newly visited city
            for city in range(num_cities):
                if not visited[city] and city != to_city:  # Exclude the current city
                    heapq.heappush(edges, (lower_triangle_matrix[max(city, to_city)][min(city, to_city)], to_city, city))

    return mst_edges
# end prim_mst

def create_tour_from_spanning_tree(spanning_tree, num_nodes, excluded_edges):
    # Create an adjacency list representation of the spanning tree
    adjacency_list = {i: [] for i in range(num_nodes)}
    for edge in spanning_tree:
        adjacency_list[edge[0]].append((edge[1], edge[2]))
        adjacency_list[edge[1]].append((edge[0], edge[2]))

    # Create a set of excluded edges for faster lookup
    excluded_edges_set = set((edge[0], edge[1]) for edge in excluded_edges)

    def dfs(current_node, visited):
        visited.add(current_node)
        neighbors = sorted(adjacency_list[current_node], key=lambda x: x[1])

        for neighbor, weight in neighbors:
            if neighbor not in visited and (current_node, neighbor) not in excluded_edges_set:
                tour.append(neighbor)
                dfs(neighbor, visited)

    start_node = 0  # You can choose any starting node
    visited_nodes = set()
    tour = [start_node]
    dfs(start_node, visited_nodes)

    return tour
# end creat tour from MST

def create_tour_from_spanning_tree2(spanning_tree, num_nodes):
    # Create an adjacency list representation of the spanning tree
    adjacency_list = {i: [] for i in range(num_nodes)}
    for edge in spanning_tree:
        adjacency_list[edge[0]].append((edge[1], edge[2]))
        adjacency_list[edge[1]].append((edge[0], edge[2]))

    def dfs(current_node, visited, tour):
        visited.add(current_node)
        neighbors = sorted(adjacency_list[current_node], key=lambda x: x[1])

        for neighbor, weight in neighbors:
            if neighbor not in visited:
                tour.append(neighbor)
                dfs(neighbor, visited, tour)

    start_node = 0  # You can choose any starting node
    visited_nodes = set()
    tour = [start_node]
    dfs(start_node, visited_nodes, tour)

    return tour
# end create tour from MST

# Performace was the same, these edges wouldn't be included in the mst anyway
# so they cant effect 2opt on the tour. Infact they made the same tour
def comp_spans(minimum_spanning_tree, lower_triangular_matrix, largest_edges):
    # run two opt add up distances, compare average
    tries = 1
    distance1 = 0
    distance2 = 0
    matrix_len = len(lower_triangular_matrix)

    for _ in range (tries):
        tour1 = create_tour_from_spanning_tree(minimum_spanning_tree, matrix_len, largest_edges)
        tour2 = create_tour_from_spanning_tree2(minimum_spanning_tree, matrix_len)
        with open("comp1.txt", 'w') as output_file:
            for city in tour1:
                output_file.write(str(city))
        
        with open("comp2.txt", 'w') as output_file:
            for city in tour2:
                output_file.write(str(city))

        _, optimized_distance1= two_opt(tour1, lower_triangular_matrix)
        _, optimized_distance2= two_opt(tour2, lower_triangular_matrix)

        distance1 += optimized_distance1    
        distance2 += optimized_distance2    
    
    if(distance1 > distance2):
        print(f"LONG edges is better: Tour1 {distance1} , Tour2 {distance2}")
    else:
        print(f"LONG edges is worse: Tour1 {distance1} , Tour2 {distance2}")
# end comp two opt
            
def print_MST(MST):
    for edge in MST:
        print(f"Edge: {edge[0]} - {edge[1]}, Weight: {edge[2]}")
# end print MST
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py file_path")
        sys.exit(1)

    file_path = sys.argv[1]

    lower_triangular_matrix = read_lower_triangular_matrix(file_path)

    full_matrix = create_full_matrix(lower_triangular_matrix)
    
    # largest_edges = find_largest_edges_per_node(lower_triangular_matrix) #O(N)

    #Find MST - O(N^2 logN) for connected?
    minimum_spanning_tree = prim_mst(lower_triangular_matrix)

    # comp_spans(minimum_spanning_tree, lower_triangular_matrix,largest_edges)

    # # Create a tour from the spanning tree- O(N^2 logN)
    tour = create_tour_from_spanning_tree2(minimum_spanning_tree, len(lower_triangular_matrix))

    output_file_name = "TSP_Output\TSP_HPrime_Out.txt"
    with open(output_file_name, 'a') as output_file:
        output_file.write(f"\n\n---- TSP HPrime Output ---- ")
        output_file.write(f"\nNumber of Cities:  {len(lower_triangular_matrix)}")
        # output_file.write(f"\n\nMST_Initial_Tour:  {tour}")

    # optimize
    start_time = time.time()
    optimized_tour = two_opt_updated(tour, full_matrix) # O(N^2)
    elapsed_time = time.time() - start_time
    optimized_distance = calculate_distance(optimized_tour,lower_triangular_matrix) # O(N)
    
    # Output the results
    with open(output_file_name, 'a') as output_file:
        output_file.write(f"\nOptimized Distance:  {optimized_distance}")
        output_file.write(f"\nExecution Time:  {elapsed_time} seconds")
        # output_file.write(f"\n\nOptimized Tour:  {optimized_tour}")  # O(N)

    print("Initial Distance:", calculate_distance(tour, lower_triangular_matrix)) # O(N)
    print("Execution Time: ", elapsed_time, "seconds")
    print("Optimized Distance:", optimized_distance)
    

