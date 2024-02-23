def read_lower_triangular_matrix(file_path):# 0(N^2 + N)?
    with open(file_path, 'r') as file:
        lines = file.readlines()  # 0(N)?

    # Split each line and convert to integers
    matrix = [list(map(int, line.split())) for line in lines]

    # Ensure the matrix is symmetric (copy lower triangular values to upper triangular)
    for i in range(len(matrix)): # 0(N)?
        for j in range(i + 1, len(matrix[i])): # 0(N)?
            matrix[j][i] = matrix[i][j]

    return matrix
# end read lower triangle

def calculate_distance(tour, lower_triangle_matrix): # O(N)
    # print(f"CD:Tour: {tour}")
    total_distance = 0
    for i in range(len(tour) - 1):
        from_city, to_city = tour[i], tour[i + 1]  # Extracting consecutive cities from the list
        try:
            distance = lower_triangle_matrix[max(from_city, to_city)][min(from_city, to_city)]
            total_distance += distance
            # print(f"Edge: ({from_city}, {to_city}), Distance: {distance}, Total Distance: {total_distance}")
        except IndexError:
            # Handle out-of-bounds indices
            print(f"IndexError: ({from_city}, {to_city})")

    # Return to the starting city
    try:
        last_edge = tour[-1]
        distance = lower_triangle_matrix[last_edge][tour[0]]
        total_distance += distance
        # print(f"Return Edge: ({last_edge}, {tour[0]}), Distance: {distance}, Total Distance: {total_distance}")
    except IndexError:
        # Handle out-of-bounds indices
        print(f"IndexError: ({last_edge}, {tour[0]})")

    return total_distance
# end calculate distance

def cost_change(cost_mat, n1, n2, n3, n4): # O(1)
    cc = cost_mat[n1][n3] + cost_mat[n2][n4] - cost_mat[n1][n2] - cost_mat[n3][n4]
    # print(f"CC_fun: {cc} ({n1} {n2} {n3} {n4}): {cost_mat[n1][n3]} + {cost_mat[n2][n4]} - {cost_mat[n1][n2]} - {cost_mat[n3][n4]}")

    return cc
# end cost

# very slow due to calculating
# full distance O(N), n^2 times
def two_opt(tour, lower_triangle_matrix): #O(N^3)
    best_distance = calculate_distance(tour, lower_triangle_matrix)
    improved = True

    while improved:
        improved = False
        for i in range(1, len(tour) - 2): #O(N)
            for j in range(i + 1, len(tour)): #O(N)
                if j - i == 1: # dont consider adjacent edges
                    continue 
                
                # O(N) + O(N) -> O(2N) -> O(N)
                new_tour = tour[:i] + tour[i:j][::-1] + tour[j:] #O(N)
                new_distance = calculate_distance(new_tour, lower_triangle_matrix) # O(N)

                # print(f"i={i}, j={j}, Old Distance={best_distance}, New Distance={new_distance}")

                if new_distance < best_distance:
                    # print("Improvement found!")
                    # print("Old Tour:", tour)
                    # print("New Tour:", new_tour)
                    # print("Old Distance:", best_distance)
                    # print("New Distance:", new_distance)

                    tour, best_distance = new_tour[:], new_distance
                    improved = True

    return tour, best_distance
# end two_opt

# credit stack overflow for faster version
def two_opt_updated(route, cost_mat): #full matrix, # O(N^3) worst case, much lower constant however
    best = route
    improved = True
    while improved: # O(N) worst case
        improved = False
        for i in range(1, len(route) - 2): # O(N)
            for j in range(i + 1, len(route)): # O(N - i)?
                if j - i == 1: continue
                cc = cost_change(cost_mat, best[i - 1], best[i], best[j - 1], best[j]) # O(1)
                if cc < 0:
                    best[i:j] = best[j - 1:i - 1:-1] # O(1)
                    improved = True
        route = best[:] # O(N)
    return best
# end two_opt_updated

def find_largest_edges_per_node(lower_triangle_matrix): # 0(N^2)?
    largest_edges_per_node = []

    for i, row in enumerate(lower_triangle_matrix): # 0(N)?
        # Exclude the diagonal elements and the current node
        non_zero_values = [value for j, value in enumerate(row[:i]) if value != 0] # 0(N)?

        if non_zero_values:
            max_edge = max(non_zero_values)
            largest_edges_per_node.append((i, row.index(max_edge), max_edge))

    return largest_edges_per_node
# end find_largest_edges_per_node

def print_matrix(matrix): # O(N)
    for row in matrix:
        print(row)
# end print matrix
        
def create_full_matrix(lower_triangle_matrix): # O(N)
    size = len(lower_triangle_matrix)

    # Create a full matrix and fill it using the lower triangular matrix
    full_matrix = [[0] * size for _ in range(size)]

    for i in range(size):
        for j in range(i + 1):
            full_matrix[i][j] = lower_triangle_matrix[i][j]
            full_matrix[j][i] = lower_triangle_matrix[i][j]

    return full_matrix
# end full matrix
