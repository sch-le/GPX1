""" track.py


Author: Amin Kamal

"""

import gpxpy.gpx
import lxml

def _get_trkpts(input_gpx: gpxpy.gpx.GPX) -> list:
    """Creates a list of all trackpoints with their associated latitude, longitude, and optional elevation

    Args:
        input_gpx (gpxpy.gpx.GPX): GPX file data

    Returns:
        list: List with latitude, longitude, elevation
    """
    
    trkpts = []
    
    # Search for all trackpoints in the GPX file
    for trk in input_gpx.tracks:
        for trkseg in trk.segments:
            for trkpt in trkseg.points:
                lat = trkpt.latitude
                lon = trkpt.longitude
                ele = trkpt.elevation if trkpt.elevation is not None else ""
                trkpts.append([lat, lon, ele])
    
    return trkpts

def print_list(input_gpx: gpxpy.gpx.GPX) -> None:
    """Prints a list of all trackpoints with their associated latitude, longitude, and optional elevation

    Args:
        input_gpx (gpxpy.gpx.GPX): GPX file data
    """
    
    print("   ID   |  Latitude  |  Longitude  |  Elevation")
    print("--------|------------|-------------|-------------")
    
    # Create a list of all trackpoints
    trkpts = _get_trkpts(input_gpx)
    
    # Print the trackpoint information in list form
    for id, trkpt in enumerate(trkpts):
        if trkpt[2] != "":
            print(f"  {id:04}  |  {trkpt[0]:9.6f} |  {trkpt[1]:9.6f}  | {trkpt[2]:9.6f}")
        else:
            print(f"  {id:04}  |  {trkpt[0]:9.6f} |  {trkpt[1]:9.6f}  | {trkpt[2]}")

def get_count(input_gpx: gpxpy.gpx.GPX) -> int:
    """Returns the number of trackpoints in the file

    Args:
        input_gpx (gpxpy.gpx.GPX): GPX file data

    Returns:
        int: Number of trackpoints
    """
    
    trkpts = _get_trkpts(input_gpx)
    
    return len(trkpts)

def calc_elevation(id1: int, id2: int, input_gpx: gpxpy.gpx.GPX) -> float:
    """Returns the elevation difference between two trackpoints

    Args:
        id1 (int): ID of the first trackpoint
        id2 (int): ID of the second trackpoint

    Returns:
        float: Elevation difference
    """
    
    trkpts = _get_trkpts(input_gpx)
    
    if not (0 <= id1 < len(trkpts)):
        print("Error 200: Trackpoint 1 not found!")
        return None
    
    if not (0 <= id2 < len(trkpts)):
        print("Error 201: Trackpoint 2 not found!")
        return None
    
    if trkpts[id1][2] == "":
        print("Error 202: No elevation information for Trackpoint 1!")
        return None
    
    if trkpts[id2][2] == "":
        print("Error 203: No elevation information for Trackpoint 2!")
        return None
    
    ele_diff = float(trkpts[id2][2]) - float(trkpts[id1][2])
    print(f"Elevation difference = {ele_diff}")
    return ele_diff

def edit(id: int, lat: float, lon: float, ele: float, input_gpx: gpxpy.gpx.GPX) -> gpxpy.gpx.GPX:
    """Changes the latitude, longitude, and elevation of a given trackpoint

    Args:
        id (int): ID of the trackpoint to edit
        lat (float): Latitude
        lon (float): Longitude
        ele (float): Elevation
        input_gpx (gpxpy.gpx.GPX): GPX file data

    Returns:
        gpxpy.gpx.GPX: Edited GPX data
    """
    
    trackpoints = list(input_gpx.walk())
    trackpoints[id].latitude = lat
    trackpoints[id].longitude = lon
    trackpoints[id].elevation = ele
    
    print_list(input_gpx)
    return input_gpx
