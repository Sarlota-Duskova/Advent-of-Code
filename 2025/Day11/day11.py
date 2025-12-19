import logging # For logging events
import os # Provides a way to interact with the operating system, such as file and directory operations.

# ------------------ Logging ------------------

logging.getLogger('urllib3').setLevel(logging.INFO) # Set up logging events.
log_level = logging.INFO # Define log level for the program.
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') 

# ------------------ File Location ------------------

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

# ------------------ File Reading ------------------

def read_file(filename):
    """
    Read the device graph from the input file.

    Each line has the form:
        aaa: bbb ccc ddd

    Meaning:
        - 'aaa' has directed edges to ['bbb', 'ccc', 'ddd']

    Returns:
        A directed adjacency list representing the graph.
    """

    graph: dict[str, list[str]] = {}

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            node, outputs = line.split(":")
            graph[node.strip()] = outputs.strip().split()

    return graph

# ------------------ Part 1 ------------------

def find_all_paths(
    graph: dict[str, list[str]],
    start: str,
    end: str
) -> list[list[str]]:
    """
    - Find all simple paths from `start` to `end` using Depth-First Search.
    - A simple path does not revisit the same node twice.

    Depth-first search - starts at the root and explores each branch to its leaf node before moving to the next branch.

    Breadth-first search - starts at the root and explores every child node, and recursively does so for every node
    """ 

    paths: list[list[str]] = []

    def dfs(node: str, path: list[str]) -> None:

        if node == end:
            paths.append(path)
            return
        
        if node not in graph:
            return
        
        for neighbor in graph.get(node, []):
            if neighbor in path:
                continue 

            dfs(neighbor, path + [neighbor])
    
    dfs(start, [start])
    return paths

def part1(graph: dict[str, list[str]]) -> int:
    """
    Part 1
    Count all paths from 'you' to 'out'.
    """

    paths = find_all_paths(graph, "you", "out")
    return len(paths)

# ------------------ Part 2 ------------------

def count_paths_with_required_nodes(
        graph: dict[str, list[str]], 
        start: str, 
        end: str, 
        required_nodes: set[str]
        ) -> int:
    """
    - Count all simple paths from `start` to `end` that pass through ALL nodes in `required_nodes`.

    Uses DFS with:
    - visited set to prevent cycles
    - tracking of required nodes encountered so far
    """

    # This will hold count of matching paths
    count = 0

    # Depth-first search
    def dfs(
        node: str, 
        visited: set[str], 
        seen_required: set[str]
        ) -> None:
        nonlocal count

        # If we reached the destination node
        if node == end:
            # If all required nodes seen on this path, increment count
            if required_nodes.issubset(seen_required):
                count += 1
            return

        # For every neighbor we can go to
        for neighbor in graph.get(node, []):
            # Skip nodes already on the current path to avoid cycles
            if neighbor  in visited:
                continue

            # Mark neighbor visited, go deeper, then unmark (backtrack)
            visited.add(neighbor)

            # Update the set of required nodes we've seen so far on this path
            new_seen = set(seen_required)
            if neighbor in required_nodes:
                new_seen.add(neighbor)

            dfs(neighbor, visited, new_seen)
            visited.remove(neighbor)

    initial_seen = {start} & required_nodes
    dfs(start, {start}, initial_seen)

    return count

def part2(graph: dict[str, list[str]]) -> int:
    """
    Part 2
    - Count all paths from 'svr' to 'out' that pass through both 'dac' and 'fft' (in any order).
    """

    required = {"dac", "fft"}

    return count_paths_with_required_nodes(
        graph,
        start="svr",
        end="out",
        required_nodes=required,
    )

# ------------------ Main ------------------

def main():
    filename_path = os.path.join(__location__, "day11.txt")
    graph = read_file(filename_path)
    #logging.info(f"Graph: {graph}")

    # Part 1
    result_part1 = part1(graph)
    logging.info(f"Part 1 - Paths from 'you' to 'out': {result_part1}")

    # Part 2
    result_part2 = part2(graph)
    logging.info(
        f"Part 2 - Paths from 'svr' to 'out' "
        f"passing through dac & fft: {result_part2}"
    )

if __name__ == "__main__":
    main()