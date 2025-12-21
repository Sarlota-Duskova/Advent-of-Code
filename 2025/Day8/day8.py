import logging
import os
from math import sqrt
from itertools import combinations
from functools import reduce
import operator

# ------------------ Logging ------------------

logging.getLogger('urllib3').setLevel(logging.INFO)
log_level = logging.INFO
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# ------------------ File Location ------------------

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

# ------------------ File Reading ------------------

def read_file(filename: str) -> list[list[int]]:
    """
    - Reads a file containing 3D coordinates of junction boxes.

    - Example line in file: "162,817,812"
    - Returns: [[162, 817, 812], [57, 618, 57], ...]
    """

    boxes: list[list[int]] = []
    
    with open(filename, "r") as file:

        for line in file:
            boxes.append(list(map(int, line.strip().split(","))))
        return boxes

# ------------------ Part 1 ------------------

def part1(boxes: list[list[int]], num_pairs: int) -> int:
    """
    Part 1
    - Connects the first `num_pairs` closest junction box pairs.
    - Returns the product of the sizes of the three largest circuits.
    
    - boxes example: [[162, 817, 812], [57, 618, 57], ...]
    """

    # Step 1: Compute all pairwise distances
    pairs = []

    for boxA, boxB in combinations(boxes, 2):
        dx = boxB[0] - boxA[0]
        dy = boxB[1] - boxA[1]
        dz = boxB[2] - boxA[2]

        dist = sqrt(dx*dx + dy*dy + dz*dz)
        pairs.append((tuple(boxA), tuple(boxB), dist)) # Each pair: ((x1,y1,z1), (x2,y2,z2), distance)

    # Step 2: Sort pairs by distance (shortest first)
    pairs.sort(key=lambda item: item[2])

    # Step 3: Union-Find (Disjoint Set) for circuits
    parent = {tuple(box): tuple(box) for box in boxes}
    size = {tuple(box): 1 for box in boxes} # {(162, 817, 812): 1, (57, 618, 57): 1, ...}

    def find(box):
        if parent[box] != box:
            parent[box] = find(parent[box])
        return parent[box]
    
    def union(boxA, boxB):
        rootA = find(boxA)
        rootB = find(boxB)
        if rootA == rootB:
            return False  # already connected
        # Union by size
        if size[rootA] < size[rootB]:
            rootA, rootB = rootB, rootA
        parent[rootB] = rootA
        size[rootA] += size[rootB]
        return True

    # Step 4: Connect the first `num_pairs` closest pairs
    for boxA, boxB, dist in pairs[:num_pairs]:
        union(boxA, boxB)

    # Step 5: Compute final circuit sizes
    circuit_sizes = list({find(box): size[find(box)] for box in parent}.values())
    circuit_sizes.sort(reverse=True)

    # Step 6: Multiply the sizes of the three largest circuits
    top_three = circuit_sizes[:3]
    product = reduce(operator.mul, top_three)

    return product

# ------------------ Part 2 ------------------

def part2(boxes: list[list[int]]) -> int:
    """
    Part 2
    - Connects junction boxes in order of shortest distance until all boxes are in one circuit.
    - Returns the product of the X coordinates of the last two boxes connected.
    """

    # Step 1: Compute all pairwise distances
    pairs = []
    for boxA, boxB in combinations(boxes, 2):
        dx = boxB[0] - boxA[0]
        dy = boxB[1] - boxA[1]
        dz = boxB[2] - boxA[2]
        dist = sqrt(dx*dx + dy*dy + dz*dz)
        pairs.append((tuple(boxA), tuple(boxB), dist))

    # Step 2: Sort pairs by distance
    pairs.sort(key=lambda item: item[2])

    # Step 3: Union-Find
    parent = {tuple(box): tuple(box) for box in boxes}
    size = {tuple(box): 1 for box in boxes}

    def find(box):
        if parent[box] != box:
            parent[box] = find(parent[box])
        return parent[box]

    def union(boxA, boxB):
        rootA = find(boxA)
        rootB = find(boxB)
        if rootA == rootB:
            return False  # already connected
        if size[rootA] < size[rootB]:
            rootA, rootB = rootB, rootA
        parent[rootB] = rootA
        size[rootA] += size[rootB]
        return True

    # Step 4: Connect boxes until all in one circuit
    total_boxes = len(boxes)
    last_connection = None

    for boxA, boxB, dist in pairs:
        if union(boxA, boxB):
            last_connection = (boxA, boxB)
            # Check if all boxes are now in one circuit
            if size[find(boxA)] == total_boxes:
                break

    # Step 5: Multiply the X coordinates of the last connected boxes
    x1, x2 = last_connection[0][0], last_connection[1][0]
    return x1 * x2

# ------------------ Main ------------------

def main():
    filename_path = os.path.join(__location__, "day8.txt")
    junctions_boxes = read_file(filename_path)
    #logging.info(f"Junctions boxes: {junctions_boxes}")

    # Part 1
    num_pairs = 1000
    part1_result = part1(junctions_boxes, num_pairs)
    logging.info(f"Part 1: {part1_result}")

    # Part 2
    part2_result = part2(junctions_boxes)
    logging.info(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()