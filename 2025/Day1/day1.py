import logging # For logging events
import os # Provides a way to interact with the operating system, such as file and directory operations. 

logging.getLogger('urllib3').setLevel(logging.INFO) # Set up logging events.

log_level = logging.INFO # Define log level for the program.
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Dynamically determine the location of the script.
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

# ------------------ File Reading ------------------

def read_file(filename: str) -> list[str]:
    """
    Read rotation instructions like 'L68' or 'R10' from a file.
    Each line represents one rotation.
    """

    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip()]
    """
        for line in file:
            line = line.strip()

            if not line:
                continue

            rotation.append(line)
    return rotation
     """
    
# ------------------ Part 1 ------------------

def count_zero_end_positions(rotations: list[str], start_position: int, dial_size: int) -> int:
    """
    Part 1
    - The dial start by pointing at 50.
    - Actual password is the number of times the dial is left pointing at 0 after any rotation in the sequence. 
    """

    current_position = start_position
    zero_hits = 0

    for rotation in rotations:
        direction = rotation[0]
        steps = int(rotation[1:])
    
        if direction == "L":
            current_position = (current_position - steps) % dial_size # 50 - 68 = -18 % 100 = 82
            
        elif direction == "R":
            current_position = (current_position + steps) % dial_size

        if current_position == 0:
            zero_hits += 1
    
    return zero_hits

# ------------------ Part 2 ------------------

def count_zero_all_clicks(rotations: list[str], start_position: int, dial_size: int) -> int:
    """
    Part 2
    - The dial start by pointing at 50.
    - Actual password is the number of times any click causes the dial to point at 0.
    """

    current_position = start_position
    zero_hits = 0

    for rotation in rotations:
        direction = rotation[0]
        steps = int(rotation[1:])
        start = current_position

        

        if direction == "L":
            # First time reaching 0 going left
            steps_to_zero = start if start != 0 else dial_size
            
            if steps >= steps_to_zero:
                zero_hits += 1 + (steps - steps_to_zero) // dial_size # (50 - 68) = -18 // 100 = 0 -> 1 + 0 = 1

            current_position = (start - steps) % dial_size

        elif direction == "R":
            wraps = (start + steps) // dial_size # 52 + 48 = 100 // 100 = 1
            zero_hits += wraps
            current_position = (start + steps) % dial_size # (52 + 48) % = 100 % 100 = 0

    return zero_hits

def main():
    filename_path = os.path.join(__location__, "day1.txt")
    rotations = read_file(filename_path)
    #logging.info(f"Rotations: {rotations}")

    start_position = 50
    dial_size = 100

    # ---- Part 1 ----
    part1 = count_zero_end_positions(rotations, start_position, dial_size)
    logging.info(f"Part 1 result: {part1}")

    # ---- Part 2 ----
    part2 = count_zero_all_clicks(rotations, start_position, dial_size)
    logging.info(f"Part 2 result: {part2}")

if __name__ == "__main__": # Entry point of the script
    main()