import logging # For logging events.
import os # Provides a way to interact with the operating system, such as file and directory operations.
from collections import deque


logging.getLogger('urllib3').setLevel(logging.INFO) # Set up logging events.

log_level = logging.INFO # Define log level for the program.
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Dynamically determine the location of the script, which allows file paths to be relative to the script's directory.
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

def read_file(filename):
    """
    Reads a file containing page ordering and updates, returning two separate lists.

    :param filename: Name of the file to read.
    :return: A tuple (page_ordering, page_updates), where:
            - page_ordering is a list of [a, b] pairs where a must come before b.
            - page_updates is a list of lists of integers representing page updates.
    """

    page_ordering = [] # Stores lines containing '|' as pairs of integers.
    page_updates = [] # Stores lines containing ',' as lists of integers.

    with open(filename, "r") as file: # Open the file in read mode.
        for line in file:
            line = line.strip() # Remove leading/ trailing whitespace.
            if not line: # Skip empty lines.
                continue

            if '|' in line: # Lines with '|' represent page ordering rules.
                page_ordering.append([int(x) for x in line.split('|')])
            elif ',' in line: # Lines with ',' represent page updates.
                page_updates.append([int(x) for x in line.split(',')])

        return page_ordering, page_updates 

def build_order_rules(page_ordering):
    """
    Creates a dictionary of ordering rules based on the page_ordering list.

    :param page_ordering: List of pairs [a, b], where a must come before b.
    :return: A dictionary mapping each page to a set of pages that must come after it.
    """

    order_rules = {}
    for a, b in page_ordering:
        if a not in order_rules:
            order_rules[a] = set() # Initialize a set if the page is not already in the dictionary.
        order_rules[a].add(b) # Add b to the set of pages that must follow a.
    return order_rules

def is_order_valid(page_ordering, update_list):
    """
    Validates if the given update list respects the page ordering rules.

    :param page_ordering: List of [a, b] pairs where a must come before b.
    :param update_list: List of pages to validate.
    :return:
        - True if the update list respects the rules.
        - False if the list cannot be reordered to respect the rules.
        - Reordered list if the order can be corrected.
    """

    order_rules = build_order_rules(page_ordering)

    # Initialize in-degree count for each page in the update list.
    in_degree = {page: 0 for page in update_list} # {97: 0, 13: 0, 75: 0, 29: 0, 47: 0}

    # Build in-degree values based on order rules.
    for page in order_rules:
        if page in update_list: # Only consider pages in the update list. Example: update_list: [97, 13, 75, 29, 47]
            for after in order_rules[page]:
                print(f"after: {after}")
                if after in update_list:
                    in_degree[after] += 1 # Increment in-degree for pages that must come after.
                    print(f"after2: {after}")
                    

    # Perform topological sort using a deque (queue).
    queue = deque([page for page in update_list if in_degree[page] == 0]) # Start with pages having in-degree 0.
    sorted_list = [] # Store the sorted order.

    while queue:
        page = queue.popleft() # Remove the first element from the queue.
        print(f"page: {page}")
        sorted_list.append(page) # Add it to the sorted list.
        print(f"sorted_list: {sorted_list}")
        if page in order_rules: # Check if the page has any dependencies.
            for after in order_rules[page]:
                if after in in_degree:
                    in_degree[after] -= 1 # Decrease in-degree of dependent pages.
                    if in_degree[after] == 0:
                        queue.append(after) # Add to the queue if in-degree becomes 0.

    # Check if the topological sort was successful.
    if len(sorted_list) == len(update_list): # All pages are sorted.
        return sorted_list if sorted_list != update_list else True # Return reordered list of True if already valid.
    return False # If not all pages are sorted, the order is invalid.


def correctly_ordered_and_reordered_sum(page_ordering, page_updates):
    """
    Calculate the sum of middle numbers for valid and reordered updates.

    :param page_ordering: List of [a, b] pairs defining ordering rules.
    :param page_updates: List of lists, each containing pages to validate.
    :return: A tuple (valid_sum, reordered_sum):
            - valid_sum is the sum of middle numbers of correctly ordered updates.
            - reordered_sum is the sum of middle numbers of reordered updates.
    """

    valid_sum = 0 # Sum for correctly ordered updates.
    reordered_sum = 0 # Sum for reordered updates.

    for update_list in page_updates:
        result = is_order_valid(page_ordering, update_list)

        if result is True: # If the update list is valid as is.
            middle_index = len(update_list) // 2
            valid_sum += update_list[middle_index] # Add the middle element to the valid sum.
        elif result is False: # If the list cannot be reordered, skip it.
            continue
        else: # If the list can be reordered.
            middle_index = len(result) // 2
            reordered_sum += result[middle_index] # Add the middle element of the reordered list.

    return valid_sum, reordered_sum

def main():
    """
    Main function to read data, validate orders, and log results.
    """

    filename_path = os.path.join(__location__, "day5_test.txt") # Construct the file path using the script's location.
    page_ordering, page_updates = read_file(filename_path) # Read the page ordering and updates from the file.
    valid_sum, reordered_sum = correctly_ordered_and_reordered_sum(page_ordering, page_updates) # Calculate the sums of middle numbers for valid and reordered updates.

    # Log the results.
    logging.info(f"Sum of middle page numbers from correctly ordered updates: {valid_sum}.")
    logging.info(f"Sum of middle page numbers from  reordered updates: {reordered_sum}.")

# Entry point of the script.
if __name__ == "__main__":
    main()