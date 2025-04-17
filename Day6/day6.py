import logging # For logging events
import os # Provides a way to interact with the operating system, such as file and directory oprerations
import numpy as np # For multi-dimensional arrays and mathematical operations.

logging.getLogger('urllib3').setLevel(logging.INFO) # Set up logging events.

log_level = logging.INFO # Define log level for the program.
# Configure the logging format to include timestamp, logger name, log level, and message.
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s -%(message)s')

# Dynamically determine the location of the script, which allows file paths to be relative to the script's directory.
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

def read_file(filename):
    """
    Reads the content of a file and returns it as a 2D NumPy array.

    :param filename: Name of the file to read.
    :return: A 2D NumPy array containing the content of the file. 
    """
    grid = [] # Initialize an empty list to store the content of the file.
    with open(filename, "r") as file: # Open the file in read mode.
        for line in file:
            grid.append(list(line.strip())) # Strip whitespace and split the line into a list of characters.
        grid_array = np.array(grid) # Convert the list of lists to a NumPy array.
        return grid_array

def patrol_path(grid, add_obstacle_pos=None):
    """
    Simulates a patrol path on a grid and tracks visited positions.

    :param grid: The grid representing the patrol area.
    :param add_obstacle_pos: Optional tuple specifying a position to add an obstacle.
    :return: A tuple with the count of visited positions and a flag indicating if a loop was detected.
    """
    # Define possible directions as vectors: (row change, column change).
    directions = {
        "^": (-1, 0),   # Up
        "v": (1,0),     # Down
        "<": (0, -1),   # Left
        ">": (0, 1)     # Right
    }

    # Define turning rules: Current direction -> Next direction when turning right.
    turns = {
        "^": ">",
        ">": "v",
        "v": "<",
        "<": "^"
    }

    obstacle = "#" # Character representing an obstacle.
    visited_position = "X" # Character representing a visited position.
    visited_positions = set() # Set to store all visited states.

    sum_visited_positions = 0 # Counter for visited positions.
    add_obstacle_hits = 0 # Counter for obstacle-related interactions.

    # Add an obstacle to the specified position if one is provided.
    if add_obstacle_pos:
        if grid[add_obstacle_pos] == ".":
            grid[add_obstacle_pos] = obstacle

    # Locate the starting position and direction.
    for idx, val in np.ndenumerate(grid):
        if val in directions:
            position = idx # Starting position as a tuple (X, Y).
            direction = val # Starting direction is '^'.
            break
    
    # Simulate the patrol path until the guard leaves the grid.
    while True:
        current_state = (position, direction)

        # Check if the current state has already been visited (loop detection).
        if current_state in visited_positions:
            if position == add_obstacle_pos:
                add_obstacle_hits += 1
            return len(visited_positions), True

        visited_positions.add(current_state) # Mark the current state as visited.
        grid[position] = visited_position # Mark the current position on the grid.

        # Calculate the next position based on the current direction. 
        next_row = position[0] + directions[direction][0]
        next_col = position[1] + directions[direction][1]
        next_position = (next_row, next_col)
        
        # If the next position is outside the grid, stop the patrol.
        if not (0 <= next_row < grid.shape[0] and 0 <= next_col < grid.shape[1]):
            # Count the total number of visited positions.
            for i in np.ndenumerate(grid):
                if i[1] == visited_position:
                    sum_visited_positions += 1
            break # The guard leaves the grid.
        
        # If the next position is an obstacle, turn right.
        if grid[next_position] == obstacle:
            direction = turns[direction]
        else:
            
            position = next_position # Move forward.

    return sum_visited_positions, False 

def find_stuck_positions(grid):
    """
    Finds positions where adding an obstacle causes the guard to get stuck in a loop.

    :param grid: The grid representing the lab.
    :return: A list of positions causing loops when obstructed.
    """

    stuck_positions = 0 # Counter for positions that cause loops.

    for idx, val in np.ndenumerate(grid):
        if val == ".": # Simulate the patrol with an obstacle at the current position.
            is_loop_detected = patrol_path(grid.copy(), add_obstacle_pos=idx)
            
            # If a loop is detected, increment the counter.
            if is_loop_detected[1] == True:
                stuck_positions += 1

    return stuck_positions

def main():
    filename_path = os.path.join(__location__,"day6_test.txt") # Define the filename path using the script's location.

    grid = read_file(filename_path) # Read the data from the file.

    visited_positions_count, is_loop_detected = patrol_path(grid.copy()) # Simulate the patrol path and log the results.
    logging.info(f"The guard visited {visited_positions_count} positions before leaving the mapped area.")
    if is_loop_detected:
        logging.info("A loop was detected during the patrol.")

    # Find positions that would cause a loop if obstructed.
    stuck_positions = find_stuck_positions(grid)
    logging.info(f"The guard would get stuck in a loop if obstacles were added at {stuck_positions} positions.")

# Entry point of the script.                
if __name__ == "__main__":
    main()
