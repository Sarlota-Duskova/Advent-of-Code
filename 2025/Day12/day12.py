import logging
import os
import re

# ------------------ Logging ------------------

logging.getLogger('urllib3').setLevel(logging.INFO)
log_level = logging.INFO
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# ------------------ File Location ------------------

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

# ------------------ File Reading ------------------

def read_file(filename: str):
    """
    Returns:
        shapes: {shape_id: ["###", "##.", "##."]}
        regions: [{"width": 4, "height": 4, "counts": [0,0,0,0,2,0]}, ...]
    """

    shapes: dict[int, list[str]] = {}
    regions: list[dict] = []

    current_shape_id = None
    current_shape_grid: list[str] = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue
            
            shape_match = re.fullmatch(r"(\d+):", line)
            if shape_match:
                # save previous shape
                if current_shape_id is not None:
                    shapes[current_shape_id] = current_shape_grid

                current_shape_id = int(shape_match.group(1))
                current_shape_grid = []
                continue
            
            if set(line) <= {'.', '#'}:
                current_shape_grid.append(line)
                continue


            region_match = re.fullmatch(r"(\d+)x(\d+):([0-9 ]+)", line)

            if region_match:
                if current_shape_id is not None:
                    shapes[current_shape_id] = current_shape_grid
                    current_shape_id = None
                    current_shape_grid = []
    
            width = int(region_match.group(1))
            height = int(region_match.group(2))
            counts = list(map(int, region_match.group(3).split()))
            regions.append({
                "width": width, 
                "height": height, 
                "counts": counts
                })
            continue


        return shapes, regions

# ------------------ Part 1 ------------------


def part1(shapes: dict[int, list[str]], regions) -> int:
    # count how many '#' each shape has
    shape_area = {}

    # Loop through all shapes
    for sid, grid in shapes.items():
        # Initialize counter for this shape
        count = 0
        
        # Loop through each row in the grid
        for row in grid:
            # Count number of '#' in this row and add to total count
            count += row.count("#")
        
        # Store the total count in the dictionary
        shape_area[sid] = count

    valid_regions = 0

    for region in regions:
        width = region["width"]
        height = region["height"]
        counts = region["counts"]

        region_area = width * height
        
        # Initialize total required area
        required_area = 0

        # Loop through all shape counts for this region
        for shape_id, count in enumerate(counts):
            # Multiply the area of this shape by how many are needed
            shape_total = shape_area[shape_id] * count

            # Add to the total required area
            required_area += shape_total

        if required_area <= region_area:
            valid_regions += 1

    return valid_regions

# ------------------ Part 1 ------------------
def part2():
    pass

# ------------------ Main ------------------

def main():
    filename_path = os.path.join(__location__, "day12.txt")
    shapes, regions = read_file(filename_path)
    #logging.info(f"Presents: {presents}")

    part1_result = part1(shapes, regions)
    logging.info(f"Part 1 - results: {part1_result}")

if __name__ == "__main__":
    main()