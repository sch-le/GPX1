import gpxpy
from gpx1 import track_module as tracks
import os

# Get the absolute path to the GPX file
gpx_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test1.gpx'))

# Load GPX file
with open(gpx_file_path, "r") as gpx_file:
    gpx_content = gpx_file.read()
    print("GPX File Content:")  # Debug print
    print(gpx_content)  # Debug print
    gpx_data = gpxpy.parse(gpx_content)

# Print track points
tracks.print_list(gpx_data)

# Get track points count
count = tracks.get_count(gpx_data)
print(f"Total track points: {count}")

# Calculate elevation difference
tracks.calc_elevation(0, 1, gpx_data)

# Edit a track point
edited_gpx = tracks.edit(0, 47.644, -122.326, 5.0, gpx_data)

# Print edited track points
tracks.print_list(edited_gpx)
