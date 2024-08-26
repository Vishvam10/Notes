import os
import re
import time
from datetime import datetime

# Updated regex pattern to match filenames with the specific timestamp format
pattern = re.compile(r"^(.*?)(?:_| )([0-9]{6})_([0-9]{6})\.(pdf|sdocx)$")

def process_file(file_path):
    match = pattern.match(os.path.basename(file_path))
    if match:
        base_name, date_part1, date_part2, extension = match.groups()

        # Extract year, month, day, hours, minutes, and seconds
        year = f"20{date_part1[:2]}"  # Assuming 21st century
        month = date_part1[2:4]
        day = date_part1[4:6]
        hour = date_part2[:2]
        minute = date_part2[2:4]
        second = date_part2[4:6]

        # Format date string for datetime.strptime
        date_str = f"{year}-{month}-{day} {hour}:{minute}:{second}"
        
        try:
            date_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            print(f"Date format error for file '{file_path}': {e}")
            return

        # Generate new file path without timestamp
        new_file_name = f"{base_name}.{extension}"
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

        # Rename the file
        os.rename(file_path, new_file_path)

        # Set the file's modification time
        timestamp = time.mktime(date_time.timetuple())
        os.utime(new_file_path, (timestamp, timestamp))

        print(f"Renamed '{file_path}' to '{new_file_path}' and set modification date to '{date_time}'.")

def run(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf") or file.endswith(".sdocx"):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    from constants import BASE_DIR

    run(BASE_DIR)
