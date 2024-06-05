"""
tracks.py



Author: Amin Kamal

"""

import gpxpy
import gpxpy.gpx

def _get_tracks(input_gpx: gpxpy.gpx.GPX) -> list:
    """Creates a list of all track points with their corresponding latitude, longitude, and optional elevation

    Args:
        input_gpx (gpxpy.gpx.GPX): Data from the GPX file

    Returns:
        list: List with latitude, longitude, elevation
    """
    
    tracks = []
    
    for track in input_gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat = point.latitude
                lon = point.longitude
                ele = point.elevation if point.elevation is not None else ""
                tracks.append([lat, lon, ele])
    
    return tracks

def print_list(input_gpx: gpxpy.gpx.GPX) -> None:
    """Prints a list of all track points with their corresponding latitude, longitude, and optional elevation

    Args:
        input_gpx (gpxpy.gpx.GPX): Data from the GPX file
    """
    
    print("   ID   |  Latitude  |  Longitude  |  Elevation")
    print("--------|------------|-------------|-------------")
    
    tracks = _get_tracks(input_gpx)
    
    for id, track in enumerate(tracks):
        if track[2] != "":
            print(f"  {id:04}  |  {track[0]:9.6f} |  {track[1]:9.6f}  | {track[2]:9.6f}")
        else:
            print(f"  {id:04}  |  {track[0]:9.6f} |  {track[1]:9.6f}  | {track[2]} ")

def get_count(input_gpx: gpxpy.gpx.GPX) -> int:
    """Returns the number of track points in the file

    Args:
        input_gpx (gpxpy.gpx.GPX): Data from the GPX file

    Returns:
        int: Number of track points
    """
    
    tracks = _get_tracks(input_gpx)
    
    return len(tracks)

def calc_elevation(id1: int, id2: int, input_gpx: gpxpy.gpx.GPX) -> float:
    """Returns the elevation difference between two track points

    Args:
        id1 (int): ID of the first track point
        id2 (int): ID of the second track point
        input_gpx (gpxpy.gpx.GPX): Data from the GPX file

    Returns:
        float: Elevation difference
    """
    
    tracks = _get_tracks(input_gpx)
    
    if not (0 <= id1 < len(tracks)):
        print("Error 200: Track point 1 not found!")
        return
    
    if not (0 <= id2 < len(tracks)):
        print("Error 201: Track point 2 not found!")
        return
    
    if tracks[id1][2] == "":
        print("Error 202: No elevation information for track point 1!")
        return
    
    if tracks[id2][2] == "":
        print("Error 203: No elevation information for track point 2!")
        return
    
    ele_diff = float(tracks[id2][2]) - float(tracks[id1][2])
    print(f"Elevation difference = {ele_diff}")
    
    return ele_diff

def edit(id: int, lat: float, lon: float, ele: float, input_gpx: gpxpy.gpx.GPX) -> gpxpy.gpx.GPX:
    """Changes the latitude, longitude, and elevation of a given track point

    Args:
        id (int): ID of the track point to edit
        lat (float): Latitude
        lon (float): Longitude
        ele (float): Elevation
        input_gpx (gpxpy.gpx.GPX): Data from the GPX file

    Returns:
        gpxpy.gpx.GPX: Edited GPX data
    """
    
    track_points = []
    for track in input_gpx.tracks:
        for segment in track.segments:
            track_points.extend(segment.points)
    
    if not (0 <= id < len(track_points)):
        print("Error 204: Track point not found!")
        return
    
    track_points[id].latitude = lat
    track_points[id].longitude = lon
    track_points[id].elevation = ele
    
    print_list(input_gpx)
    return input_gpx
