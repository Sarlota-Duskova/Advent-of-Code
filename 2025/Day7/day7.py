import logging
import os

# ------------------ Logging ------------------

logging.getLogger('urllib3').setLevel(logging.INFO)
log_level = logging.INFO
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# ------------------ File Location ------------------

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

# ------------------ File Reading ------------------

def read_file(filename: str) -> list[str]:

    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip()]


# ------------------ Part 1 ------------------
def part1(tachyon_manifold):
    """
    - Represent beam as (row, col), only current beam position
    - A set or list of active beams
    - Start with one beam just below S
    """

    rows = len(tachyon_manifold)
    cols = len(tachyon_manifold[0])

    for r in range(rows):
        if "S" in tachyon_manifold[r]:
            start_row = r
            start_col = tachyon_manifold[r].index("S")
            break
    
    # Start with one beam just below S
    beams = {(start_row + 1, start_col)}
    split_count = 0

    """
    For each beam:
    - if it exits the grid -> discard it
    - if it enters . -> keep going
    - if it enters ^:
        - increment the split counter
        - remove the curreant beam
        - create two new beams
            - one at (row+1, col-1)
            - one at (row+1, col+1)
        - only keep new beams that are inside the grid
    """

    while beams:
        next_beams = set()

        for r, c in beams:
            if r >= rows or c < 0 or c >= cols:
                continue 

            cell = tachyon_manifold[r][c]

            if cell == "." or cell == "S":
                # Beam continues downward
                next_beams.add((r + 1, c))

            elif cell == "^":
                # Beam splits
                split_count += 1
                next_beams.add((r + 1, c - 1))
                next_beams.add((r + 1, c + 1))

        """
        - Handle beam merging, if multiple beams land on the same cell - keep only one beam
        """
        beams = next_beams

    return split_count
    
# ------------------ Part 2 ------------------

def part2(tachyon_manifold):
    

    rows = len(tachyon_manifold)
    cols = len(tachyon_manifold[0])

    # Step 1: Find the startin postion "S"
    for r in range(rows):
        if "S" in tachyon_manifold[r]:
            start_row = r
            start_col = tachyon_manifold[r].index("S")
            break

    # Step 2: Memo    
    memo = {}

    # Step 3: Recursive function
    def count_timelines(r, c):
        # Exits grid
        if r >= rows or c < 0 or c >= cols:
            return 1
        
        # Memo check
        if (r, c) in memo:
            return memo[(r, c)]

        cell = tachyon_manifold[r][c]
        
        if cell == "." or cell== "S":
            result = count_timelines(r + 1, c)

        elif cell == "^":
            result = count_timelines(r + 1, c - 1) + count_timelines(r + 1, c + 1)

        else:
            result = count_timelines(r + 1, c) 
    
        memo[(r, c)] = result
        return result
    
    
    # Step 5: Start recursion just below "S"
    total_timelines = count_timelines(start_row + 1, start_col)
    return total_timelines


# ------------------ Main ------------------

def main():
    filename_path = os.path.join(__location__, "day7.txt")
    tachyon_manifold = read_file(filename_path)
    #logging.info(f"Tachyon manifold: {tachyon_manifold}")

    # Part 1
    part1_result = part1(tachyon_manifold)
    logging.info(f"Part 1: {part1_result}")

    # Part 2
    part2_result = part2(tachyon_manifold)
    logging.info(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()