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

def read_file(filename: str) -> tuple[list[tuple[int, int]], list[int]]:
    """
    Reads the inventory database file.

    Returns:
        fresh_ranges: list of (start, end) tuples
        available_ids: list of ingredient IDs
    """

    fresh_ranges: list[tuple[int, int]] = []
    available_ids: list[int] = []

    with open(filename, "r") as file:
        lines = [line.strip() for line in file]

    reading_ranges = True

    for line in lines:
        if line == "":
            reading_ranges = False
            continue

        if reading_ranges:
            start, end = map(int, line.split("-"))
            fresh_ranges.append((start, end))
        else:
            available_ids.append(int(line))

    return fresh_ranges, available_ids

# ------------------ Part 1 ------------------

def count_fresh_available_ids(
        fresh_ranges: list[tuple[int, int]],
        available_ids: list[int,]
        ) -> int:
    """
    Part 1
    Count how many available ingredient IDs are fresh.
    """

    fresh_count = 0

    for ingredient_id in available_ids:
        for start, end in fresh_ranges:
            if start <= ingredient_id <= end:
                fresh_count += 1
                break
    
    return fresh_count

# ------------------ Part 2 ------------------

def count_total_fresh_ids(fresh_ranges: list[tuple[int, int]]) -> int:
    """
    Part 2
    Count how many distinct ingredient IDs are covered by the union of all fresh ranges.
    """
    
    if not fresh_ranges:
        return 0
    
    # Sort ranges by starting value
    sorted_ranges = sorted(fresh_ranges)

    total = 0
    current_start, current_end = sorted_ranges[0]

    # Initialize the current merged range using the first range (e.g. 3–5)
    for start, end in sorted_ranges[1:]: # Iterate over the remaining ranges, e.g. [(10, 14), (12, 18), (16, 20)]
        # Check if the current range overlaps with or directly touches the previous one
        if start <= current_end + 1: # Example: 10 <= 5 + 1 → False (no overlap)
            current_end = max(current_end, end) # Extend the current merged range if necessary
        else:
            # No overlap: finalize the previous merged range
            total += current_end - current_start + 1 # Example: (5 - 3 + 1) = 3 values
            current_start, current_end = start, end # Start a new merged range

    total += current_end - current_start + 1 # Add the final merged range
    return total

# ------------------ Main ------------------

def main():
    filename_path = os.path.join(__location__, "day5.txt")
    fresh_ranges, available_ids = read_file(filename_path)
    #logging.info(f"Ingrediends list: {fresh_ranges, available_ids}")

    # ---- Part 1 ----
    part1 = count_fresh_available_ids(fresh_ranges, available_ids)
    logging.info(f"Part 1: Fresh available ingredient IDs = {part1}")

    # ---- Part 2 ----
    part2 = count_total_fresh_ids(fresh_ranges)
    logging.info(f"Part 2: Total fresh ingredient IDs = {part2}")

if __name__== "__main__":
    main()