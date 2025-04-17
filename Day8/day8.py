import logging # For logging events.
import os # Provides a way to interact with the operating system, such as file and directory operations.
import numpy as np # For multi-dimensional arrays and mathematical operations.

logging.getLogger('urllib3').setLevel(logging.INFO) # Set up logging events.

log_level = logging.INFO # Define log level for the program.
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Dynamically determine the location of the script, which allows file paths to be relative to the script's directory.
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

def read_file(filename):
    grid = [] # Initialize an empty list

    # Read the file
    with open(filename, "r") as file:
        for line in file:
            grid.append(list(line.strip()))
        grid_array = np.array(grid)
    return grid_array

def main():
    filename_path = os.path.join(__location__, "day8_test.txt") # Define the filename using the script's location. 

    test = read_file(filename_path) 
    print(test)
    #result =
    # logging.info(f"{}") 

# Entry point of the script.
if __name__ == "__main__":
    main()