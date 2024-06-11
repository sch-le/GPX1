"""track.py

(c) PaFeLe²KyLuKa-Industries

Description: Functions for reading and editing tracks
Author: Leon Schuck
Created: 01.06.2024
"""

from gpx1.config import gpx
import lxml
from gpx1.usefull import print_color, print_error

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
    
    print_color("  Track-ID  |  Name    ")
    print_color("------------|----------")
    
    # Creates List of all tracks with their corrosponding tracksegments and trackpoints
    trks = _get_trks(input_gpx)
    
    for id, trk in enumerate(trks):
        print_color(f"  {id:4}      |  {trk[id]}")

def print_list_trksegs(trk: int, input_gpx: gpx) -> None:
    """_summary_

    Args:
        input_gpx (gpx): _description_
    """
    
    # Creates List of all tracks with their corrosponding tracksegments and trackpoints
    trks = _get_trks(input_gpx)
    
    if not (0 <= trk < len(trks)):
        print_error("Error 300: Track außerhalb des gültigen Bereichs")
        return False
    
    print_color(" Tracksegment-ID | Trackpoints   ")
    print_color("-----------------|---------------")
    
    for id, trkseg in enumerate(trks[trk][1]):
        print_color(f"  {id:4}           |  {len(trkseg):5}        ")
    
    return True

def print_list_trkpts(trk: int, trkseg: int, input_gpx: gpx) -> None:
    """Prints a list of all trackpoints with their corresponding latitude, longitude, and optional elevation.

    Args:
        input_gpx (gpx): Data from the GPX file
    """
    
    # Creates List of all tracks with their corrosponding tracksegments and trackpoints
    trks = _get_trks(input_gpx)
    
    if not (0 <= trkseg < len(trks[trk][1])):
        print_error("Error 301: Tracksegment ausserhalb des gültigen Bereichs!")
        return False
    
    print_color("   ID   |  Latitude  |  Longitude  |  Elevation  ")
    print_color("--------|------------|-------------|-------------")

    # Print trackpoint information in list form
    for id, trkpt in enumerate(trks[trk][1][trkseg]):
        if trkpt[2] != "":
            print_color(f"  {id:04}  |  {trkpt[0]:9.6f} |  {trkpt[1]:9.6f}  | {trkpt[2]:9.6f}")
        else:
            print_color(f"  {id:04}  |  {trkpt[0]:9.6f} |  {trkpt[1]:9.6f}  | {trkpt[2]}")
            
    return True

def get_count(input_gpx: gpx) -> int:
    """Returns the number of tracks/tracksegments/trackpoints in the file.

    Args:
        input_gpx (gpx): Data from the GPX file

    Returns:
        int: Number of trackpoints
    """
    trkpts = _get_trks(input_gpx)
    return len(trkpts)

def edit(trk_id: int, trkseg_id: int, trkpt_id: int, lat: float, lon: float, ele: float, input_gpx: gpx) -> gpx:
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
    
    # Find the specific "trkpt" element
    trks = _get_trks(input_gpx)

    # Überprüfung ob Waypoint existiert
    if not (0 <= trkpt_id < len(trks[trk_id][1][trkseg_id])):
        print_error("Error 304: Waypoint nicht vorhanden!")
        return
    
    # Bereichsüberprüfung der Latitude
    if not (0 <= lat <= 90):
        print_error("Error 302: Latitude außerhalb des erlaubten Bereichs!  0 <= Latitude <= 90")
        return
    
    # Bereichsüberprüfung der Longitude
    if not (0 <= lon <= 180):
        print_error("Error 303: Latitude außerhalb des erlaubten Bereichs! 0 <= Longitude <= 180")
        return
    
    # Find the specific Waypoint
    trk = input_gpx.etree.findall("{*}trk")[trk_id]
    trkseg = trk.findall("{*}trkseg")[trkseg_id]
    trkpt = trkseg.findall("{*}trkpt")[trkpt_id]
    
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
    
    return input_gpx
