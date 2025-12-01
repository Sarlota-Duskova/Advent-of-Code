import logging # For logging events.
import os # Provides a way to interact with the operating system, such as file and directory operations.
from itertools import product # Utilities for Cartesian products.

logging.getLogger('urllib3').setLevel(logging.INFO) # Set up logging events.

log_level = logging.INFO # Define log level for the program.
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Dynamically determine the location of the script, which allows file paths to be relative to the script's directory.
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

def read_file(filename):
    """
    Reads a file containing test values and numbers, and returns them as separate lists.

    :param filename: The name of the file to read.
    :return: A tuple (test_values, numbers), where:
            - test_values is a list of integers representing the target values. 
            - numbers is a list of lists of integers representing the numbers to be evaluated. 
    """

    test_values = [] # List to store target values (numbers before ":").
    numbers = [] # List to store lists of numbers (numbers after ":").

    with open(filename, "r") as file: # Open the file in read mode.
        for line in file:
            line = line.strip() # Remove leading/ trailing whitespace.
            if not line: # Skip empty lines.
                continue
            if ':' in line: # Check if the line contains ":".
                parts = line.split(":") 
                test_values.append(int(parts[0].strip())) # Extract the number before ":".
                numbers.append([int(x) for x in parts[1].strip().split()]) # Extract the numbers after ":", split them, and convert to integers.

        return test_values, numbers

def evaluate_expression(nums, operators):
    """
    Evaluates an expression based on the given numbers and operators.

    :param nums: List of integers to be evaluated.
    :param operators: List of operators to apply between the numbers.
    :return: The result of evaluating the expression.
    """

    result = nums[0] # Initialize the result with the first number.
    
    # Iterate over the operators and apply them to the numbers sequentially.
    for i in range(len(operators)):
        if operators[i] == "+": # Addition operator.
            result += nums[i + 1]
        elif operators[i] == "*": # Multiplication operator.
            result *= nums[i + 1]
        elif operators[i] == "||": # Concatenation operator.
            result = int(str(result) + str(nums[i + 1])) # Concatenate the numbers as strings and convert back to integer.
    return result

def calibration(test_values, numbers):
    """
    Finds the sum of all test values for which a valid equation exists.

    :param test_values: List of target values to achieve.
    :param numbers: List of lists of numbers to use in the equations. 
    :return: The total sum of the test values for which a valid equation exists.
    """

    operators = ["+", "*", "||"] # Supported operators: addition, multiplication, and concatenation.
    total = 0 # Initialize the total sum.


    for test_value, nums in zip(test_values, numbers): # Iterate over the test values and corresponding lists of numbers.
        for operator in product(operators, repeat=len(nums) -1): # Generate all possible combinations of operators for the given numbers.
            result = evaluate_expression(nums, operator) # Evaluate the expression using the current combination of operators.
            if result == test_value: # Check if the result matches the test value.
                total += test_value # Add the test value to the total sum.
                logging.info(f"Equation found: {nums} with operators {operator} = {test_value}") # Log the matching equation for debugging purposes.
                break # Stop checking further combinations for this test value.
    return total

def main():
    filename_path = os.path.join(__location__, "day7_test.txt") # Define the filename using the script's location.
    test_values, numbers = read_file(filename_path) # Read the test values and numbers from the file.
    result = calibration(test_values, numbers) # Perform the calibration to find the total sum of valid test values.
    logging.info(f"Total calibration result is {result}.") # Log the total calibration result.

# Entry point of the script.    
if __name__ == "__main__":
    main()