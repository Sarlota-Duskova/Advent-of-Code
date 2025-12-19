import logging
import os
import re
from itertools import combinations
from collections import deque

# ------------------ Logging ------------------

logging.getLogger('urllib3').setLevel(logging.INFO)
log_level = logging.INFO
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# ------------------ File Location ------------------

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

# ------------------ File Reading ------------------

def read_file(filename:str) -> tuple[list[str], list[str], list[str]]:
    """
    Reads input file for Day 10 and returns:
    - machines: List of indicator light strings (e.g., ".##.")
    - buttons: List of button wiring strings (e.g., "(0,1) (2)")
    - joltages: List of target joltage strings (e.g., "3,5,4,7")
    """
    
    machines: list[str] = []
    buttons: list[str] = []
    joltages: list[str] = []

    pattern = r"\[(.*?)\]\s*((?:\([^)]*\)\s*)+)\{(.*?)\}"

    with open(filename, "r") as file:
        for line in file:
            line = line.rstrip("\n")
            
            reg = re.search(pattern, line)
            if not reg:
                continue

            machines.append(reg.group(1))
            buttons.append(reg.group(2))
            joltages.append(reg.group(3))

    return machines, buttons, joltages

# ------------------ Part 1 ------------------

# ------------------ Machine to bits ------------------

def machine_to_bits(machine: str) -> list[int]:
    """Convert indicator string like '.##.' to a list of bits [0,1,1,0]."""
    return [1 if c == "#" else 0 for c in machine]

# ------------------ Button Parsing ------------------

def parse_buttons(buttons_str: str) -> list[list[int]]:
    """
    Converts a button string "(0,1) (2,3)" into a list of lists of integers [[0,1],[2,3]]
    """

    result: list[list[int]] = []
    groups = re.findall(r"\(([^)]*)\)", buttons_str)

    for g in groups:
        if not g.strip():
            continue

        nums = [int(x) for x in (part.strip() for part in g.split(",")) if x != ""]
        result.append(nums)

    return result

def min_presses_lights(machine: str, buttons_str: str) -> int:
    """Find minimum presses to reach target indicator light pattern."""
    target = machine_to_bits(machine)
    buttons = parse_buttons(buttons_str)
    n = len(buttons)

    for k in range(1, n + 1):
        for combo in combinations(range(n), k):
            state = [0] * len(target)
            for i in combo:
                for idx in buttons[i]:
                    state[idx] ^= 1  # toggle
            if state == target:
                return k
    # fallback (should not happen)
    return 0

def part1(machines: list[str], buttons_list: list[str]) -> int:
    total = 0
    for idx, machine in enumerate(machines):
        presses = min_presses_lights(machine, buttons_list[idx])
        total += presses
    return total

# ------------------ Part 2 ------------------

# ------------------ Joltage Parsing ------------------

def parse_joltages(joltage_str: str) -> list[int]:
    """
    Converts a string like "3,5,4,7" into [3,5,4,7]
    """

    return [int(x) for x in joltage_str.split(",")]

def min_presses_joltage(buttons: list[list[int]], target: list[int]) -> int:
    # Breadth-First Search (BFS)
    """
    - Is a graph traversal algorithm that starts from a source node and explores the graph level by level. First, it visits all nodes directly adjacent to the source. Then, it moves on to visit the adjacent nodes of those nodes, and this process continues until all reachable nodes are visited.
    """

    start = [0] * len(target)
    queue = deque()
    queue.append((start, 0))
    visited = set()
    visited.add(tuple(start))
    
    while queue:
        state, presses = queue.popleft()

        if state == target:
            return presses
        
        for button in buttons:
            #next_state = press_joltage(state, button)
            next_state = state[:]

            for i in button:
                next_state[i] += 1

            if any(next_state[i] > target[i] for i in range(len(target))):
                continue

            key = tuple(next_state)

            if key not in visited:
                visited.add(key)
                queue.append((next_state, presses + 1))

    return -1

def part2(buttons_list: list[str], joltages_list: list[str]) -> int:

    total = 0

    for idx in range(len(buttons_list)):
        buttons = parse_buttons(buttons_list[idx])
        target = parse_joltages(joltages_list[idx])
        presses = min_presses_joltage(buttons, target)
        total += presses

    return total

# ------------------ Main ------------------

def main():
    filename_path = os.path.join(__location__, "day10.txt")
    machines, buttons_list, joltages_list = read_file(filename_path)
    logging.info(f"Input: {machines, buttons_list, joltages_list}")

    # Part 1: indicator lights
    result_part1 = part1(machines, buttons_list)
    logging.info(f"Part 1 - Minimum presses for indicator lights: {result_part1}")

    # Part 2: joltage counters
    result_part2 = part2(buttons_list, joltages_list)
    logging.info(f"Part 2 - Minimum presses for joltage counters: {result_part2}")

if __name__ == "__main__":
    main()