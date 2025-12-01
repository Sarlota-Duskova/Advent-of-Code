import logging # For logging events.
import re # ReGex module for pattern matching within the memory string. 
import os # Provides a way to interact with the operating system, such as file and directory opreations.

logging.getLogger('urllib3').setLevel(logging.INFO) # Set up logging events.

log_level = logging.INFO # Define log level for the program.
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s -%(levelname)s - %(message)s')

# Dynamically determine the location of the script, which allows file paths to be relative to the script's directory.
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

def read_file(filename):
    """
    Reads the content of a file and returns it as a 2D array.

    :param filename: Name of the file to read.
    :return: String containing the content of the file.
    """
    array2D = [] # Initialize an empty list to store the content
    with open(filename, "r") as file: # Open the file in read mode.
        for line in file:
            array2D.append(list(line.strip()))
        return array2D # Return the file content.

def ceres_search(matrix, word):
    """
    Counts occurrences of the word in all 8 directions.
    """
    rows = len(matrix)
    cols = len(matrix[0])
    word_len = len(word)

    directions = [
        (0, 1), # Right
        (0, -1), # Left
        (1, 0), # Down
        (-1, 0), # Up
        (1, 1), # Diagonal Down-Right
        (1, -1), # Diagonal Down-Left
        (-1, 1), # Diagonal Up-Right
        (-1, -1) # Diagonal Up-Left
    ]
    occurrences = 0 

    # Function to check if a word exists starting at (row, col) in a specific direction
    def check_direction(row, col, dir_x, dir_y):
        for i in range(word_len):
            new_row = row + i * dir_x
            new_col = col + i * dir_y
            # Check if indices are within bounds and character matches
            if new_row < 0 or new_row >= rows or new_col < 0 or new_col >= cols or matrix[new_row][new_col] != word[i]:
                return False
        return True
    
    # Traverse each cell in the matrix
    for row in range(rows):
        for col in range(cols):
            # Check all 8 directions from the current cell
            for dir_x, dir_y in directions:
                if check_direction(row, col, dir_x, dir_y):
                    occurrences += 1
    return occurrences

def find_xmas(matrix):
    """
    Counts occurrences of the X-MAS pattern (MAS/SAM forming an X).
    """
    rows = len(matrix)
    cols = len(matrix[0])
    patterns = ["MAS", "SAM"]
    count = 0

    def check_diagonal(center_row, center_col):
        for pattern in patterns:
            if (center_row - 1 >= 0 and center_col - 1 >= 0 and
                center_row + 1 < rows and center_col + 1 < cols and
                matrix[center_row - 1][center_col - 1] == pattern[0] and
                matrix[center_row][center_col] == pattern[1] and
                matrix[center_row + 1][center_col + 1] == pattern[2]):
                if (
                    matrix[center_row - 1][center_col + 1] == pattern[0] and
                    matrix[center_row + 1][center_col - 1] == pattern[2]
                ):
                    return True
        return False
    
    for row in range(1, rows - 1): # Avoid borders
        for col in range(1, cols - 1): # Avoid borders
            if check_diagonal(row, col):
                count += 1
    return count

def main():
    filename_path = os.path.join(__location__, "day4_test.txt") # Define the filename using the script's location 

    word = "XMAS"
    matrix = read_file(filename_path) # Read the data from the file.
    
    # Count word occurrences in all directions 
    word_count = ceres_search(matrix, word)
    logging.info(f"The word {word} occurs: {word_count} times in all directions.")

    # Count X-MAS patterns 
    xmas_count = find_xmas(matrix)
    logging.info(f"The X-MAS pattern appears: {xmas_count} times.")

if __name__ == "__main__":
    main()