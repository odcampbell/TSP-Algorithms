import random
import time

# Purpose: To generate graphs (lower tringular matrix form) for testing
# Results: Creates graphs more favorable to nearest neighbor

SIZE = 1000
def generate_lower_triangle_matrix(size): # O(N^2)
    lower_triangle_matrix = [[0] * (i + 1) for i in range(size)]

    for i in range(size):
        for j in range(i + 1):
            if i != j:
                lower_triangle_matrix[i][j] = random.randint(1, SIZE)  # Adjust the range w/ size

    return lower_triangle_matrix

def write_triangle_matrix_to_file(matrix, filename): # O(N^2)
    with open(filename, 'w') as file:
        for i, row in enumerate(matrix):
            # Set the diagonal to 0
            row[i] = 0
            # Convert non-zero elements to strings
            non_zero_elements = [str(element) for element in row]
            file.write(' '.join(non_zero_elements) + '\n')
# end write triangle matrix
            
def make_N_graphs(num_cities):

    for size in range(500, num_cities, 500): # O(N/500)?
        start_time = time.time()
        matrix = generate_lower_triangle_matrix(size) # O(N^2)
        fileName = f"Graphs\g{size}M.txt"
        write_triangle_matrix_to_file(matrix, fileName) # O(N^2)
        elapsed_time = time.time() - start_time

        print(f"Elapsed Time on {fileName}: {elapsed_time} s")
# end make_N_graphs

# Example usage:
num_cities = 1000
make_N_graphs(num_cities)