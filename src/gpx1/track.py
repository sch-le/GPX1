"""track.py

(c) PaFeLe²KyLuKa-Industries

Description: Functions for reading and editing tracks
Author: Leon Schuck
Created: 01.06.2024
"""

from gpx1.config import gpx
import lxml
from gpx1.usefull import print_color

def _get_trks(input_gpx: gpx) -> list:
    """Creates a list of all tracks with trackpoints with their corresponding latitude, longitude, and optional elevation.

    Args:
        input_gpx (gpx): Data from the GPX file

    Returns:
        list: List of latitude, longitude, elevation
    """
    trks = []
    i = 0
    # Find all trackpoints in the GPX file
    for trk in input_gpx.etree.findall("{*}trk"):
        trks.append([])
        name = trk.find("{*}name").text
        trks[i].append(name)
        trks[i].append([])
        n = 0 
        for trkseg in trk.findall("{*}trkseg"):
            trks[i][1].append([])
            for trkpt in trkseg.findall("{*}trkpt"):
                lat = float(trkpt.get("lat"))
                lon = float(trkpt.get("lon"))
                ele = ""
                if trkpt.find("{*}ele") is not None:
                    ele = float(trkpt.find("{*}ele").text)
                trks[i][1][n].append([lat, lon, ele])
            n = n + 1
        i = i + 1
    return trks

def print_list_trks(input_gpx: gpx) -> None:
    """_summary_

    Args:
        input_gpx (gpx): _description_
    """
    print_color("  Track |  Name    ")
    print_color("--------|----------")
    
    # Creates List of all tracks with their corrosponding tracksegments and trackpoints
    trks = _get_trks(input_gpx)
    
    for id, trk in enumerate(trks):
        print_color(f"  {id:4}  |  {trk[id]}")

def print_list_trksegs(i, input_gpx: gpx) -> None:
    """_summary_

    Args:
        input_gpx (gpx): _description_
    """
    print_color("   Tracksegmente   ")
    print_color("-------------------")
    
    # Creates List of all tracks with their corrosponding tracksegments and trackpoints
    trks = _get_trks(input_gpx)
    
    if not (0 <= i < len(trks)):
        return
    
    for id, trkseg in enumerate(trks[i][1]):
        print_color(f"  {id:4}  ")

def print_list_trkpts(input_gpx: gpx) -> None:
    """Prints a list of all trackpoints with their corresponding latitude, longitude, and optional elevation.

    Args:
        input_gpx (gpx): Data from the GPX file
    """
    print("   ID   |  Latitude  |  Longitude  |  Elevation  ")
    print("--------|------------|-------------|-------------")
    
    # Create a list of all trackpoints
    trkpts = _get_trks(input_gpx)
    
    # Print trackpoint information in list form
    for id, trkpt in enumerate(trkpts):
        if trkpt[2] != "":
            print(f"  {id:04}  |  {trkpt[0]:9.6f} |  {trkpt[1]:9.6f}  | {trkpt[2]:9.6f}")
        else:
            print(f"  {id:04}  |  {trkpt[0]:9.6f} |  {trkpt[1]:9.6f}  | {trkpt[2]}")

def get_count(input_gpx: gpx) -> int:
    """Returns the number of tracks/tracksegments/trackpoints in the file.

    Args:
        input_gpx (gpx): Data from the GPX file

    Returns:
        int: Number of trackpoints
    """
    trkpts = _get_trks(input_gpx)
    return len(trkpts)

#def calc_elevation(id1: int, id2: int, input_gpx: gpx) -> float:
#    """Returns the elevation difference between two trackpoints.
#
#    Args:
#        id1 (int): ID of the first trackpoint
#        id2 (int): ID of the second trackpoint
#
#    Returns:
#        float: Elevation difference
#    """
#    trkpts = _get_trkpts(input_gpx)
#    
#    if not (0 <= id1 < len(trkpts)):
#        print("Error 200: Trackpoint 1 not found!")
#        return
#    
#    if not (0 <= id2 < len(trkpts)):
#        print("Error 201: Trackpoint 2 not found!")
#        return
#    
#    if trkpts[id1][2] == "":
#        print("Error 202: No elevation information for Trackpoint 1!")
#        return
#    
#    if trkpts[id2][2] == "":
#        print("Error 203: No elevation information for Trackpoint 2!")
#        return
#    
#    ele_diff = float(trkpts[id2][2]) - float(trkpts[id1][2])
#    print(f"Elevation difference = {ele_diff}")
#    return ele_diff

def edit(id: int, lat: float, lon: float, ele: float, input_gpx: gpx) -> gpx:
    """Edits the latitude, longitude, and elevation of a given trackpoint.

    Args:
        id (int): ID of the trackpoint to edit
        lat (float): Latitude
        lon (float): Longitude
        ele (float): Elevation
        input_gpx (gpx): Data from the GPX file

    Returns:
        gpx: Edited GPX data
    """
    trkpts = _get_trks(input_gpx)

    if not (0 <= id < len(trkpts)):
        print("Error 204: Trackpoint not found!")
        return
    
    # Find the specific "trkpt" element
    trkpt = input_gpx.etree.findall("{*}trk/{*}trkseg/{*}trkpt")[id]
    
    # Edit the latitude and longitude using the attributes "lat" and "lon"
    if lat is not None:
        trkpt.set("lat", str(lat))
        
    if lon is not None:
        trkpt.set("lon", str(lon))
    
    if ele is not None:
        try:
            # Edit the elevation using the child element "ele", if it exists
            trkpt.find("{*}ele").text = str(ele)
        except Exception:
            # Create the child element "ele"
            trkpt.append(lxml.etree.Element("ele"))
            trkpt.find("{*}ele").text = str(ele)
    
    #print_list(input_gpx)
    return input_gpx
