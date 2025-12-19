import logging # For logging events
import os # Provides a way to interact with the operating system, such as file and directory operations.
from math import prod

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
    Read the worksheet as raw rows (strings).
    """

    with open(filename, "r") as file:
        return [line.rstrip("\n") for line in file]

# ------------------ Part 1 ------------------

def parse_columns_left_to_right(rows: list[str]) -> list[list[int | str]]:
    """
    Parse problems column-by-column (Part 1).

    Each column represents one problem:
    - Numbers stacked vertically
    - Operator at the bottom
    """

    split_rows: list[list[int | str]] = []

    for row in rows:
        split_rows.append([int(x) if x.isdigit() else x
                           for x in row.split()])
        # [[123, 328, 51, 64], [45, 64, 387, 23], [6, 98, 215, 314], ['*', '+', '*', '+']]

    max_columns = max(len(row) for row in split_rows)

    columns: list[list[int | str]] = []

    for col_index in range(max_columns):
        column = []
        for row in split_rows:
            if col_index < len(row):
                column.append(row[col_index])
        columns.append(column)

    # [[123, 45, 6, '*'], [328, 64, 98, '+'], [51, 387, 215, '*'], [64, 23, 314, '+']]
    return columns

def part1(columns: list[list[int | str]]) -> int:
    """
    Part 1
    Evaluate all problems left-to-right and sum results.
    """

    problem_results = []

    for column in columns:
        operator = column[-1]
        values = column[:-1]

        if operator == '+':
            result = sum(values)
        elif operator == '*':
            result = prod(values)
        else:
            raise ValueError(f"Unknown operator: {operator}")

        problem_results.append(result)

    return sum(problem_results)

# ------------------ Part 2 ------------------

def parse_columns_right_to_left(rows: list[str]) -> list[str]:
    """
    Pad rows to equal length, read columns from right to left (Part 2).
    """

    max_width = max(len(row) for row in rows)
    # ['123 328  51 64 ', ' 45 64  387 23 ', '  6 98  215 314', '*   +   *   +  ']
    return [line.ljust(max_width) for line in rows]

def part2(rows: list[str]) -> int:
    """
    Part 2
    Evaluate all problems left-to-right and sum results.
    """
    
    operator_row = rows.pop() # "*   +   *   +"
    operators = operator_row.split() # ['*', '+', '*', '+']

    total = 0
    current_numbers: list[int] = []

    # Iterate from rightmost column to leftmost
    for col_idx in range(len(rows[0]) - 1, -2, -1): # range(start, stop, step)
        # len(rows[0]) = number of characters (columns)
        # - 1 → last valid index (because indexing starts at 0)
        # step = -1 -> Move right → left

        # Column break or end reached
        if col_idx == -1 or all(row[col_idx] == " " for row in rows):
            if current_numbers:
                operator = operators.pop()
                if operator == '+':
                    total += sum(current_numbers)
                elif operator == '*':
                    total += prod(current_numbers)
            current_numbers = []
        else:
            # Build number from top to bottom
            digits = ''.join(row[col_idx] for row in rows).strip()
            current_numbers.append(int(digits))

    return total

# ------------------ Main ------------------

def main():
    filename_path = os.path.join(__location__, "day6.txt")
    rows = read_file(filename_path)
    #logging.info(f"Rows: {rows}")

    # Part 1
    columns = parse_columns_left_to_right(rows)
    part_1_result = part1(columns)
    logging.info(f"Part 1 - Grand total: {part_1_result}")

    # Part 2
    padded_rows = parse_columns_right_to_left(rows)
    part_2_result = part2(padded_rows)
    logging.info(f"Part 2 - Grand total: {part_2_result}")

if __name__ == "__main__":
    main()  