import logging # For logging events
import os # Provides a way to interact with the operating system, such as file and directory operations

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
    Read the list of tile coordinates from the input file.
    """

    tiles: list[str] = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                tiles.append(line)

    return tiles

# ------------------ Part 1 ------------------

def parse_red_tiles(tiles: list[str]) -> set[tuple[int, int]]:
    """
    Parse tile strings into a set of red tile coordinates.
    """

    red_tiles: set[tuple[int, int]] = set()

    for tile in tiles:
        x_str, y_str = tile.split(",")
        red_tiles.add((int(x_str), int(y_str)))

    return red_tiles

def part1(tiles: list[str]) -> int:
    """
    Part 1
    Find the largest rectangle area using red tiles as opposite corners.
    """

    red_tiles = parse_red_tiles(tiles)
    max_area = 0

    for x1,y1 in red_tiles:
        for x2,y2 in red_tiles:
            if x1 != x2 and y1 != y2:
                area = ((abs(x2 - x1))+1) * ((abs(y2 - y1))+1)
                max_area = max(max_area, area)
    return max_area

# ------------------ Part 2 ------------------

def build_edge_green_tiles(red_tiles: list[tuple[int, int]]) -> set[tuple[int, int]]:
    """
    Build green tiles along the edges connecting consecutive red tiles.
    """

    green_tiles: set[tuple[int, int]] = set()
    n = len(red_tiles)

    for i in range(n):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % n]

        if x1 == x2: # vertical sehment
            for y in range(min(y1, y2), max(y1, y2) + 1):
                    green_tiles.add((x1, y))
        elif y1 == y2:  # horizontal segment
            for x in range(min(x1, x2), max(x1, x2) + 1):
                green_tiles.add((x, y1))
                
    return green_tiles

def point_in_polygon(x,y, polygon):
    """
    Ray-casting algorithm to check if a point is inside a polygon.
    """

    inside = False
    n = len(polygon)

    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]

        if ((y1 > y) != (y2 > y)):
            x_intersect = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x < x_intersect:
                inside = not inside

    return inside

def fill_interior(red_tiles):
    """
    Return interior tiles inside the polygon formed by red tiles.
    """

    xs = [x for x, _ in red_tiles]
    ys = [y for _, y in red_tiles]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    interior = set()

    for x in range(min_x, max_x +1):
        for y in range(min_y, max_y +1):
            if point_in_polygon(x + 0.5, y + 0.5, red_tiles):
                interior.add((x, y))

    return interior

def part2(tiles: list[str]) -> int:
    """
    Part 2
    Find largest rectangle area using red tiles as opposite corners and including green tiles.
    """

    red_tiles_list = [(int(x), int(y)) for x, y in (tile.split(",") for tile in tiles)]
    red_tiles_set = set(red_tiles_list)

    green_edges = build_edge_green_tiles(red_tiles_list)
    green_interior = fill_interior(red_tiles_list)

    allowed_tiles: set[tuple[int,int]] = red_tiles_set | green_edges | green_interior

    max_area = 0

    for x1,y1 in red_tiles_set:
        for x2,y2 in red_tiles_set:
            if x1 == x2 or y1 == y2:
                continue

            valid = True
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    if (x, y) not in allowed_tiles:
                        valid = False
                        break

                    if not valid:
                        break

            if valid:
                area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                max_area = max(max_area, area)

    return max_area

# ------------------ Main ------------------

def main():
    filename_path = os.path.join(__location__, "day9.txt")
    tiles = read_file(filename_path)

    # Part 1
    result_part1 = part1(tiles)
    logging.info(f"Part 1 - Largest rectangle (red only): {result_part1}")

    # Part 2
    result_part2 = part2(tiles)
    logging.info(f"Part 2 - Largest rectangle (red + green): {result_part2}")

if __name__ == "__main__":
    main()