import logging # For logging events.
import os # Provides a way to interact with the operating system, such as file and directory operations.

logging.getLogger('urllib3').setLevel(logging.INFO) # Set up logging events.

log_level = logging.INFO # Define log level for the program.
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s -%(message)s')

# Dynamically determine the location of the script, which allows file paths to be relative to the script's directory.
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

def read_file(filename):
    """
    Reads the content of a file and returns it as a string.

    :param filename: Name of the file to read.
    :return: String containing the content of the file.
    """
    with open(filename, "r") as file: # Open the file in read mode.
        content = file.read() # Read the entire content of the file.    
    return content # Return the file content.

def parse_disk_map(disk_map):
    """
    Parse the disk map string into a list representing disk blocks.

    :param disk_map: String containing alternating file sizes and free spaces.
    :return: List of disk blocks where integers represent file IDs and None represents free space.
    """
    blocks = []
    file_id = 0

    # Process the input string in pairs of file size and free space.
    for i in range(0, len(disk_map), 2):
        file_size = int(disk_map[i]) # Extract file size.
        free_space = int(disk_map[i + 1]) if i + 1 < len(disk_map) else 0 # Extract free space or assume 0.

        blocks.extend([file_id] * file_size) # Add file blocks to the list.
        blocks.extend([None] * free_space) # Add free space blocks (represented by None) to the list.

        if file_size > 0: # Increment the file ID if a file was added.
            file_id += 1
    return blocks

def compact_files_single_block(blocks):
    """
    Perform a compaction of the disk blocks by shifting all file blocks to the start, leaving free space blocks at the end.

    :param blocks: List of disk blocks.
    :return: Compacted list of disk blocks.
    """

    compacted = [block for block in blocks if block is not None] # Collect all non-free blocks.
    free_space = len(blocks) - len(compacted) # Calculate the remaining free space.

    compacted.extend([None] * free_space) # Append the free space blocks to the end.
    return compacted

def compact_files_whole_file(blocks):
    """
    Perform a compaction of the disk blocks by moving entire files into the first available free spaces.

    :param blocks: List of disk blocks.
    :return: Compacted list of disk blocks.
    """

    file_spans = {} # Dictionary to store start and end indices of each file.
    free_spans = [] # List to store ranges of free space.
    start = 0

    # Identify spans of files and free space in the blocks.
    while start < len(blocks):
        if blocks[start] is None: # Identify free space.
            end = start
            while end < len(blocks) and blocks[end] is None:
                end += 1
            free_spans.append((start, end)) # [(9, 18), (23, 26), (34, 41), (48, 50), (59, 61), (70, 74)]
            start = end
        else: # Identify file span.
            file_id = blocks[start]
            end = start
            while end < len(blocks) and blocks[end] == file_id:
                end += 1
            # file_spans = {0: (0, 9), 1: (18, 23), 2: (26, 34), 3: (41, 48), 4: (50, 59), 5: (61, 70), 6: (74, 75)}
            file_spans[file_id] = (start, end) # Record the file span.
            start = end 

    # Move files into free spaces if possible, starting from the largest file ID.
    for file_id in sorted(file_spans.keys(), reverse=True):
        # file_spans.keys() => dict_keys([0, 1, 2, 3, 4, 5, 6])
        file_start, file_end = file_spans[file_id]
        file_length = file_end - file_start

        # Try to fit the file into a free space span.
        for free_start, free_end in free_spans:
            free_length = free_end - free_start
            if free_length >= file_length and free_start < file_start: # Ensure space is large enough and earlier.
                blocks[free_start:free_start + file_length] = [file_id] * file_length # Move the file to the free space.
                blocks[file_start:file_end] = [None] * file_length # Clear the old file location.

                # Update the free space spans.
                free_spans.remove((free_start, free_end))
                if free_start + file_length < free_end:
                    free_spans.append((free_start + file_length, free_end))
                free_spans.sort() # Keep spans sorted for efficient processing.
                break
    return blocks

def calculate_checksum(blocks):
    """
    Calculate the checksum of the disk map by summing the product of positions and file IDs.
    
    :param blocks: List of disk blocks.
    :return: Integer checksum value.
    """
    return sum(pos * file_id for pos, file_id in enumerate(blocks) if file_id is not None)

def main():
    """
    Main function to process the disk map and compute checksums for different compaction methods.
    """
    filename_path = os.path.join(__location__, "day9.txt") # Define the filename using the script's location.
    disk_map = read_file(filename_path) # Read the disk map from the file.
    blocks = parse_disk_map(disk_map) # Parse the disk map into blocks.

    # Perform single-block compaction and calculate its checksum.
    compacted_single_block = compact_files_single_block(blocks)
    checksum_part1 = calculate_checksum(compacted_single_block)
    logging.info(f"The resulting filesystem checksum for part 1 is: {checksum_part1}.")

    # Perform whole-file compaction and calculate its checksum. 
    compacted_whole_file = compact_files_whole_file(blocks)
    checksum_part2 = calculate_checksum(compacted_whole_file)
    logging.info(f"The resulting filesystem checksum for part 2 is: {checksum_part2}.")

if __name__ == "__main__":
    main()