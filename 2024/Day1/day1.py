import logging # For logging events.
import os # Provides a way to interact with the operating system, such as file and directory operations.

logging.getLogger('urllib3').setLevel(logging.INFO) # Set up logging events.

log_level = logging.INFO # Define log level for the program.
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Dynamically determine the location of the script.
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

def read_file(filename):
    # Read the file and return two lists for columns.
    lst1 = [] # Initialize an empty list to store the first column's values.
    lst2 = [] # Initialize an empty list to store the second column's values.

    # Read the file
    with open(filename, "r") as file: # Open the file in read mode.
        for line in file: # Iterate over each line in the file.
            clm1, clm2 = map(int, line.strip().split()) # Split the line into two values, remove extra whitespace, and convert to integers.
            lst1.append(clm1) # Append the first column's value to lst1.
            lst2.append(clm2) # Append the second column's value to lst2.

    return lst1, lst2 # Return the two lists containing the values from the file.

def part1(lst1, lst2):
    total_distance = 0 # Initialize the total distance to 0.

    while lst1 and lst2: # Continue until both lists are empty.
        # Find the smallest value in lst1.
        smallest1 = min(lst1) 
        smallest2 = min(lst2) 
        total_distance += abs(smallest1 - smallest2) # Add the absolute difference between the smallest values to total_distance.

        # Remove the smallest elements to avoid reuse.
        lst1.remove(smallest1)
        lst2.remove(smallest2)

    return total_distance # Return the calculated total distance.

def part2(lst1, lst2):
    similarity_score = 0 # Initialize the similarity score to 0.

    for number in lst1: # Iterate through each number in lst1.
        count_occurrences = lst2.count(number) # Count how many times the current number appears in lst2.
        similarity_score += number * count_occurrences # Add the product of the number and its occurrence count to similarity_score.

    return similarity_score # Return the calculated similarity score.

filename_path = os.path.join(__location__, 'day1.txt') # Define the filename using the script's location.

lst1, lst2 = read_file(filename_path) # Read the file.
result1 = part1(lst1, lst2) # Compute the total distance using part1.
lst1, lst2 = read_file(filename_path) # Re-read the file to reset lst1 and lst2 for part2.
result2 = part2(lst1, lst2) # Compute the similarity score using part2. 
logging.info(f"Total distance: {result1}") # Output the total distance.
logging.info(f"Similarity score: {result2}") # Output the similarity score. 