import logging # For logging events.
import re # ReGex module for pattern matching within the memory string.
import os # Provides a way to interact with the operating system, such as file and directory operations.

logging.getLogger('urllib3').setLevel(logging.INFO) # Set up logging events.

log_level = logging.INFO # Define log level for the program.
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Dynamically determine the location of the script, which allows file paths to be relative to the script's directory.
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

def read_file(filename):
    """
    Reads the content of a file and returns it as a string.

    :param filename: Name of the file to read.
    :return: String containing the content of the file.
    """
    with open(filename, "r") as file: # Open the file in read mode.
       content = file.read() # Read the entire content of the file.
    return content # Return the file content.

def corrupted_memory(memory):
    """
    Processes the corrupted memory to find and compute all 'mul(x,y)' patterns.

    :param memory: String containing the memory data.
    :return: Total sum of all valid 'mul(x,y)' computations.
    """
    regex = r"mul\((\d+),(\d+)\)" # Regex to match 'mul(x,y)' pattern, where x and y are integers.
    matches = re.findall(regex, memory) # Find all valid matches for the pattern in the memory string.
    #print(matches)
    total = 0 # Initialize the total sum of results to 0. 

    # Process each match found in the memory string.
    for match in matches:
        x, y = map(int, match) # Convert the captured strings into integers.
        result = x * y # Compute the multiplication of x and y.
        logging.info(f"Found mul({x},{y}), result: {result}")
        total += result # Add the result to the total sum.
    return total # Return the total sum of all valid 'mul(x,y)' computations.

def part2(memory):
    regex = r"(do\(\)|don't\(\)|mul\((\d+),(\d+)\))" # Regex to match 'do()', 'don't()', or 'mul(x,y)' patterns.
    matches = re.findall(regex, memory) # Find all valid matches for the pattern in the memory string.

    is_enabled = True # By default, 'mul' instructions are enabled.
    total = 0 # Initialize the total sum of results to 0.

    # Iterate over all matches and process instructions accordingly.
    for match in matches:
        instruction = match[0]

        if instruction == "do()": # Handle enabling of 'mul' operations.
            is_enabled = True # Enable 'mul' operations.
            logging.info("Encountered do(), enabling mul operations.")

        elif instruction == "don't()": # Handle disabling of 'mul' operations.
            is_enabled = False # Disable 'mul' operations.
            logging.info("Encountered don't(), disabling mul opreations.")

        else: # This must be a 'mul(x, y)' instruction.
            if is_enabled: # Execute if 'mul' operations are enabled.
                x, y = int(match[1]), int(match[2]) # Extract and convert numbers to integers.
                result = x * y
                logging.info(f"Executing mul({x},{y}), result: {result}")
                total += result # Add the result to the total sum.
            else:
                logging.info(f"Skipping mul({match[1]},{match[2]}) as mul is disabled.")

    return total # Return the total sum of all valid 'mul(x,y)' computations. 

filename_path = os.path.join(__location__, "day3.txt") # Define the filename using the script's location.

data = read_file(filename_path) # Read the corrupted memory data from the file.
 # Process the memory data to calculate the total sum.
result = corrupted_memory(data)
result2 = part2(data)
logging.info(f"Total sum of valid mul instructions: {result}")
logging.info(f"Total sum of enabled mul instructions: {result2}")