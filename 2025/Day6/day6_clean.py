import logging # For logging events
import os # Provides a way to interact with the operating system, such as file and directory operations.
import csv

logging.getLogger('urllib3').setLevel(logging.INFO) # Set up logging events.
log_level = logging.INFO # Define log level for the program.
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') 

# Dynamically determine the location of the script.
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

def read_file(filename):
    """Original method: read rows and transpose to columns (left-to-right, top-to-bottom)."""
    rows_list = []
    with open(filename, "r") as file:
        reader = csv.reader(file, delimiter=' ')
        for row in reader:
            if row:
                rows_list.append(row)
                
    for index, sheet in enumerate(rows_list):
        numbers = []
        for elm in sheet:
            if elm != '':
                parsed_value = elm
                
                try:
                    parsed_value = int(elm)
                except ValueError:
                    pass 

                numbers.append(parsed_value)
        rows_list[index] = numbers
    
    max_cols = max(len(row) for row in rows_list) if rows_list else 0
    
    columns_list = []
    for col_index in range(max_cols):
        column = []
        for row in rows_list:
            if col_index < len(row):
                column.append(row[col_index])
        columns_list.append(column)
    return columns_list


def read_file_rightleft_columns(filename):
    """New method: read file where numbers are in right-to-left columns with top-to-bottom digits.
    
    Each column is a separate number (most significant digit at top).
    Empty columns (all spaces) separate problems.
    Last row is the operator.
    
    Returns a list of problems, where each problem is [num1, operator, num2, operator, ...]
    """
    with open(filename, "r") as file:
        lines = file.readlines()
    
    if not lines:
        return []
    
    # Remove trailing newlines but keep the structure
    lines = [line.rstrip('\n') for line in lines]
    
    # Find the maximum line length to ensure we process all columns
    max_len = max(len(line) for line in lines) if lines else 0
    
    # Pad all lines to the same length
    lines = [line.ljust(max_len) for line in lines]
    
    # Extract operator row (last line)
    operator_row = lines[-1]
    data_lines = lines[:-1]
    
    # Process each column position (left-to-right, but we'll reverse at the end for right-to-left reading)
    columns_data = []
    
    for col_idx in range(max_len):
        # Extract digit/character from each row at this column
        column_chars = [line[col_idx] if col_idx < len(line) else ' ' for line in data_lines]
        operator_char = operator_row[col_idx] if col_idx < len(operator_row) else ' '
        
        # Check if this column is empty (all spaces in data and operator)
        is_empty = all(c == ' ' for c in column_chars) and operator_char == ' '
        
        if not is_empty:
            # Non-empty column = part of the problem
            # Build the number from top-to-bottom (most significant digit first)
            number_str = ''.join(c for c in column_chars if c != ' ')
            if number_str:
                columns_data.append((int(number_str), operator_char))
            else:
                columns_data.append((None, operator_char))
        else:
            # Empty column = separator between problems
            columns_data.append(('SEPARATOR', None))
    
    # Now build problems from right-to-left (reverse the column order)
    columns_data.reverse()
    
    problems = []
    current_problem = []
    
    for number, operator in columns_data:
        if number == 'SEPARATOR':
            if current_problem:
                problems.append(current_problem)
                current_problem = []
        else:
            if number is not None:
                current_problem.append(number)
            if operator in ['+', '*']:
                current_problem.append(operator)
    
    if current_problem:
        problems.append(current_problem)
    
    return problems


def grand_total_original(columns):
    """Calculate grand total from original left-to-right column format."""
    col_sums = []
    for column in columns:
        operator = column[-1]
        numbers = column[:-1]
        col_sum = numbers[0] if numbers else 0
        
        for num in numbers[1:]:
            if operator == '+':
                col_sum += num
            elif operator == '*':
                col_sum *= num
        col_sums.append(col_sum)
    return sum(col_sums), col_sums


def grand_total_rightleft(problems):
    """Calculate grand total from right-to-left problem format (part 2)."""
    problem_results = []
    for problem in problems:
        result = problem[0] if problem else 0
        i = 1
        while i < len(problem):
            operator = problem[i]
            if i + 1 < len(problem):
                operand = problem[i + 1]
                if operator == '+':
                    result += operand
                elif operator == '*':
                    result *= operand
                i += 2
            else:
                i += 1
        problem_results.append(result)
    return sum(problem_results), problem_results


def main():
    # Part 1: Original left-to-right columns
    filename_path = os.path.join(__location__, "day6_test.txt")
    worksheets = read_file(filename_path)
    total_part1, results_part1 = grand_total_original(worksheets)
    logging.info(f"Part 1 - Grand total: {total_part1}")
    
    # Part 2: Right-to-left columns
    problems = read_file_rightleft_columns(filename_path)
    logging.info(f"Part 2 - Problems (first few): {problems[:5]}")
    total_part2, results_part2 = grand_total_rightleft(problems)
    logging.info(f"Part 2 - Problem results (first few): {results_part2[:5]}")
    logging.info(f"Part 2 - Grand total: {total_part2}")
    
if __name__ == "__main__":
    main()
