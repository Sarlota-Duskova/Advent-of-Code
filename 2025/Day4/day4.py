import logging # For logging events
import os # Provides a way to interact with the operating system, such as file and directory operations
import numpy as np
from scipy.signal import convolve2d

logging.getLogger('urllib3').setLevel(logging.INFO) # Set up logging events.
log_level = logging.INFO # Define log level for the program.
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') 

# Dynamically determine the location of the script.
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

# ------------------ File Reading ------------------

def read_file(filename):
    """
    Reads the grid of paper rolls from a file.
    Each row in the file corresponds to a list of characters ('.' or '@').
    """

    with open(filename, "r") as file:
        return [list(line.rstrip("\n")) for line in file if line.rstrip("\n")]

# ------------------ Part 1 ------------------

def accessible_paper_rolls(grid):
    """
    Part 1
    Counts the number of rolls that can be accessed by forklifts.
    A roll is accessible if it has fewer than 4 neighboring rolls ('@').
    """

    arr = np.array(grid)
    mask_rolls = (arr == '@').astype(int)

    # Define 3x3 kernel to count 8 neighbors around each cell
    neighbor_kernel = np.array([[1, 1, 1],
                    [1, 0, 1],
                    [1, 1, 1]])

    # Convolve mask with kernel to count @ around each position
    neighbor_count = convolve2d(mask_rolls, neighbor_kernel, mode='same', boundary='fill', fillvalue=0)

    accessible_mask = (neighbor_count < 4) & (mask_rolls == 1)
    accessible_count = np.sum(accessible_mask)

    return int(accessible_count)

# ------------------ Part 2 ------------------

def total_removable_paper_rolls(grid):
    """
    Part 2
    Calculates the total number of rolls that can be removed iteratively.
    Once a roll is removed, new rolls may become accessible.
    """

    arr = np.array(grid)

    # Define 3x3 kernel to count 8 neighbors around each cell
    mask_kernel = np.array([[1, 1, 1],
                    [1, 0, 1],
                    [1, 1, 1]])

    total_removed = 0
    working_grid = arr.copy()
    
    while True:
        mask_rolls = (working_grid == '@').astype(int)

        # Convolve mask with kernel to count @ around each position
        neighbor_count = convolve2d(mask_rolls, mask_kernel, mode='same', boundary='fill', fillvalue=0)
        to_remove = (neighbor_count < 4) & (mask_rolls == 1)
        num_to_remove = np.sum(to_remove)

        if num_to_remove == 0:
            break

        total_removed += num_to_remove
        working_grid[to_remove] = '.'

    return int(total_removed)

# ------------------ Main ------------------

def main():
    filename_path = os.path.join(__location__, "day4.txt")
    paper_grid = read_file(filename_path)
    #logging.info(f"Paper grid: {paper_grid}")

    # ---- Part 1 ----
    part1 = accessible_paper_rolls(paper_grid)
    logging.info(f"Accessed paper roles by a forklift: {part1}")

    # ---- Part 2 ----
    part2 = total_removable_paper_rolls(paper_grid)
    logging.info(f"Paper rolls that can be removed in total by a forklift: {part2}")

if __name__ == "__main__":
    main()