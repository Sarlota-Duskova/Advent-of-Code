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
    Read a single-line file with ID ranges separated by commas.
    """

    with open(filename, "r") as file:
        line = file.readline()

    ranges = [r.strip() for r in line.split(",") if r.strip()]
    return ranges

# ------------------ Part 1 ------------------

def is_repeated_twice(s: str) -> bool:
    """
    Returns True if the string is composed of a block repeated exactly twice.
    """

    length = len(s)

    for block_size in range(1, length // 2 + 1):
        if length == 2 * block_size and s[:block_size] * 2 == s:
            return True
    return False

def find_invalid_ids_part1(id_ranges: list[str]) -> dict[str, list[int]]:
    """Part 1
    - IDs made of a 1, 2, or 3 digit sequence repeated twice.
    """

    invalid_by_range = {}

    for id_range in id_ranges:
        if '-' not in id_range:
            logging.debug(f"Skipping invalid range token: {id_range}")
            continue
        start_str, end_str = id_range.split('-', 1)

        # Reject ranges that use leading zeros (e.g. '0101').
        if (len(start_str) > 1 and start_str.startswith('0')) or (len(end_str) > 1 and end_str.startswith('0')):
            logging.warning(f"Skipping range with leading zeros: {id_range}")
            continue

        try:
            start = int(start_str)
            end = int(end_str)
        except ValueError:
            logging.warning(f"Skipping invalid numeric range: {id_range}")
            continue

        # Ensure start <= end; otherwise skip the range and inform the user
        if start > end:
            logging.warning(f"Skipping range where start > end: {id_range}")
            continue

        invalid_ids = []
        for num in range(start, end + 1):
            s = str(num)
            # Exclude strings with leading zeros (IDs with leading zeros are not valid at all).
            if len(s) > 1 and s.startswith('0'):
                continue
            
            if is_repeated_twice(s):
                invalid_ids.append(num)

        invalid_by_range[id_range] = invalid_ids
        
    return invalid_by_range

# ------------------ Part 2 ------------------

def is_repeated_block(s: str) -> bool:
        """
        Returns True if the string is composed of a block repeated at least twice.
        Example: '1212', '123123', '111111', '12341234'.
        """
        
        length = len(s)

        if length < 2:
            return False
        
        for block_size in range(1, length // 2 + 1): # 2 // 2 = 1 -> 1 + 1 = 2
            if length % block_size == 0 and s == s[:block_size] * (length // block_size):
                # Example: 11
                # length % block_size -> 2 % 1 = 0 -> 0 == 0
                # s[:block_size] -> s[:1] = "1"
                # (length // block_size) = 2 // 1 = 2
                # s[:block_size] * (length // block_size) -> "1" * 2 = "11"
                return True
        return False

def find_invalid_ids_part2(id_ranges: list[str]) -> dict[str, list[int]]:
        """
        Part 2
        Invalid IDs are any number formed by repeating a block at least twice.
        """

        invalid_by_range = {}

        for id_range in id_ranges:
            if '-' not in id_range:
                continue

            start_str, end_str = id_range.split('-', 1)

            if (len(start_str) > 1 and start_str.startswith('0')) or (len(end_str) > 1 and end_str.startswith('0')):
                continue

            try:
                start = int(start_str)
                end = int(end_str)
            except ValueError:
                continue

            if start > end:
                continue

            invalids_ids = []

            for num in range(start, end + 1):
                s = str(num)
                if len(s) > 1 and s.startswith('0'):
                    continue
                if is_repeated_block(s):
                    invalids_ids.append(num)

            invalid_by_range[id_range] = invalids_ids

        return invalid_by_range

# ------------------ Main ------------------

def main():
    filename_path = os.path.join(__location__, "day2.txt")
    id_ranges = read_file(filename_path)
    #logging.info(f"ID ranges: {id_ranges}")

    # ---- Part 1 ----
    invalid_ids_part1 = find_invalid_ids_part1(id_ranges) # {'11-22': [11, 22], '95-115': [99],
    all_invalid_ids_part1 = [num for ids in invalid_ids_part1.values() for num in ids] # [11, 22, 99, 1010, 1188511885, 222222, 446446, 38593859]
    logging.info(f"Part 1: Sum of invalid IDs: {sum(all_invalid_ids_part1)}")

    # ---- Part 2 ----
    invalid_ids_part2 = find_invalid_ids_part2(id_ranges)
    all_invalid_ids_part2 = [num for ids in invalid_ids_part2.values() for num in ids]
    logging.info(f"Part 2: Sum of invalid IDs: {sum(all_invalid_ids_part2)}")
    
if __name__ == "__main__":
    main()  