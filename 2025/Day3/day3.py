import logging # For logging events
import os # Provides a way to interact with the operating system, such as file and directory operations.
from itertools import combinations

# ------------------ Logging ------------------

logging.getLogger('urllib3').setLevel(logging.INFO) # Set up logging events.
log_level = logging.INFO # Define log level for the program.
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') 

# ------------------ File Location ------------------

# Dynamically determine the location of the script.
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

# ------------------ File Reading ------------------

def read_file(filename: str) -> list[str]:
    """
    Read battery banks from a file. Each line is a bank of batteries represented as digits.
    Returns a list of strings, each string is a bank.
    """

    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip()]

# ------------------ Part 1 ------------------

def largest_joltage_two_batteries(banks: list[str]) -> int:
    """
    Part 1
    - Each bank has digits representing batteries.
    - Turn on exactly 2 batteries per bank to get the largest possible number.
    - Returns the sum of largest joltage from all banks.
    """


    total_output = 0

    for bank in banks:
        # Generate all 2-digit combinations of the bank
        possible_joltages = [int("".join(pair)) for pair in combinations(bank, 2)]
        total_output += max(possible_joltages)

    return total_output

# ------------------ Part 2 ------------------

def largest_joltage_k_batteries(banks: list[str], k: int) -> tuple[list[int], int]:
    """
    Part 2
    - Each bank has digits representing batteries.
    - Turn on exactly 'k' batteries per bank to get the largest possible number while preserving their order in the bank.
    
    Returns a tuple:
        - List of largest numbers per bank
        - Total sum across all banks
    """

    results: list[int] = []
    total_output: int = 0
    
    for bank in banks:
        if len(bank) < k:
            logging.warning(f"Bank length ({len(bank)}) is less than k ({k})")
            continue
        
        selected_digits: list[str] = []
        start_idx = 0
        remaining = k  # Digits still needed
        
        while remaining > 0:
            # How many digits are left in the bank from start_idx 
            digits_left = len(bank) - start_idx
            
            # How far I can look ahead to find the max digit
            max_skip = digits_left - remaining 
            
            # Find the maximum digit in the range [start_idx, start_idx + max_skip]
            max_digit = -1
            max_idx = start_idx
            for i in range(start_idx, start_idx + max_skip + 1):
                if int(bank[i]) > max_digit:
                    max_digit = int(bank[i])
                    max_idx = i

            
            selected_digits.append(str(max_digit))
            start_idx = max_idx + 1
            remaining -= 1
        
        # Convert selected digits to a number
        number = int(''.join(selected_digits))
        results.append(number)
        total_output += number
    
    return results, total_output


def main():
    filename_path = os.path.join(__location__, "day3.txt")
    battery_banks = read_file(filename_path)
    #logging.info(f"Battery banks: {battery_banks}")

    # ---- Part 1 ----
    total_part1 = largest_joltage_two_batteries(battery_banks)
    logging.info(f"Part1: Total output joltage: {total_part1}")

    # ---- Part 2 ----
    k_batteries = 12
    results_part2, total_part2 = largest_joltage_k_batteries(battery_banks, k_batteries)
    logging.info(f"Part 2: Total output joltage: {total_part2}") 

if __name__ == "__main__":
    main()