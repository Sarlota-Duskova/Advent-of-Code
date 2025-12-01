import logging # For logging events.
import numpy as np # For numerical operations and array manipulations. 
import os # Provides a way to interact with the operating system, such as file and directory operations.

logging.getLogger('urllib3').setLevel(logging.INFO) # Set up logging events.

log_level = logging.INFO # Define log level for the program.
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Dynamically determine the location of the script.
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

def read_file(filename):
    """
    Reads a file containing lists of numbers and returns a list of lists.

    :param filename: Name of the file to read.
    :return: List of lists of integers, where each sublist represents a line in the file.
    """
    nums =[] # Initialize an empty list to store the lists of numbers.
    with open(filename, "r") as file: # Open the file in read mode.
        for line in file: # Iterate through each line in the file. 
            numbers = list(map(int, line.split())) # Convert the line into a list of integers.
            nums.append(numbers) # Append the list of integers to the main list.
        return nums # Return the list of lists.
    
# Function to check if list is strictly increasing.
def is_increasing(report):
    """
    Check if a given list of numbers is strictly increasing and the differences between adjacent elements are between 1 and 3.

    :param report: List of integers.
    :return: True if the list is strictly increasing with allowed differences, False otherwise. 
    """
    diff_list = np.diff(report) # Calculate the differences between adjacent elements.
    return np.all(diff_list > 0) and np.all((diff_list >= 1) & (diff_list <= 3)) # Check if conditions are met.

# Function to check if list is strictly decreasing.
def is_decreasing(report):
    """
    Checks if a given list of numbers is strictly decreasing and the differences between adjacent elements are between -3 and -1. 

    :param report: List of integers. 
    :return: True if the list is strictly decreasing with allowed differences, False otherwise. 
    """
    diff_list = np.diff(report) # Calculate the differences between adjacent elements.
    return np.all(diff_list < 0) and np.all((diff_list <= -1) & (diff_list >= -3)) # Check if conditions are met.

def safe_reports(reports):
    """
    Determines the number of safe reports in the input. A report is safe if:
    - It is strictly increasing or strictly decreasing without modifications.
    - It can be made strictly increasing or decreasing by removing one element.

    :param reports: List of lists of integers (reports).
    :return: Tuple containing counts of safe reports without changes and with changes.
    """
    safe_reports_without_changes = 0 # Counter for reports safe without any changes. 
    safe_reports_with_changes = 0 # Counter for reports safe with at most one change. 
    # Check if all elements in the list are in increasing order.
    for report in reports:
        logging.info(f"Original list: {report}")

        if is_increasing(report) or is_decreasing(report):
            logging.info(f"Safe without changes: {report}")
            safe_reports_without_changes += 1
            safe_reports_with_changes += 1  # Already safe, so count it for both categories.
            continue # Move to the next report.

        # Check if the report can be made safe by removing one element.
        for i in range(len(report)):
            modified_report = np.delete(report, i) # Create a modified report by removing one element.
            if is_increasing(modified_report) or is_decreasing(modified_report):
                logging.info(f"Safe after removing element {report[i]}: {modified_report}")
                safe_reports_with_changes += 1
                break  # No need to check further modifications for this report.

    return safe_reports_without_changes, safe_reports_with_changes # Return the counts.

filename_path = os.path.join(__location__, 'day2.txt') # Define the filename using the script's location.

data = read_file(filename_path) # Read the input data from the specified file.
safe_reports_without_changes, safe_reports_with_changes = safe_reports(data)  # Determine safe reports.
logging.info(f"Safe reports without changes: {safe_reports_without_changes}")
logging.info(f"Safe reports (including changes): {safe_reports_with_changes}")