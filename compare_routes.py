def compare_files(file_path1, file_path2):
    try:
        with open(file_path1, 'r') as file1, open(file_path2, 'r') as file2:
            content1 = file1.read()
            content2 = file2.read()

            if content1 == content2:
                print("The contents of the files are identical.")
            else:
                print("The contents of the files are different.")
    except FileNotFoundError:
        print("One or both files not found.")

# file_path_a = 'MST1.txt'
# file_path_b = 'MST2.txt'
file_path_a = 'comp1.txt'
file_path_b = 'comp2.txt'
compare_files(file_path_a, file_path_b)