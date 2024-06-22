"""track.py

(c) PaFeLe²KyLuKa-Industries

Description: Functions for reading and editing tracks
Author: Ameen Kamal, Leon Schuck
Created: 01.06.2024
"""

import lxml

from gpx1.config import gpx
from gpx1.usefull import print_color, print_error

def _get_trks(input_gpx: gpx) -> list:
    """# Creates List of all tracks with their corrosponding tracksegments, trackpoints and latitude, longitude and elevation

    Args:
        input_gpx (gpx): Data from the GPX file

    Returns:
        list: List of latitude, longitude, elevation
    """
    
    """List of all tracks with their corrosponding tracksegments, trackpoints and latitude, longitude and elevation
    Format: [   [name_trk_0,    [   [trkseg_0_trckpoint_0_lat][trkseg_0_trckpoint_0_lon][trkseg_0_trckpoint_0_ele],
                                    ...
                                    [trkseg_0_trckpoint_n_lat][trkseg_0_trckpoint_n_lon][trkseg_0_trckpoint_n_ele],
                                ], 
                                ...
                                [   [trkseg_n_trckpoint_0_lat][trkseg_n_trckpoint_0_lon][trkseg_n_trckpoint_0_ele],  
                                    ...
                                    [trkseg_n_trckpoint_n_lat][trkseg_n_trckpoint_n_lon][trkseg_n_trckpoint_n_ele],  
                                ],
                ],
                ...
                [name_trk_n,    [   [trkseg_0_trckpoint_0_lat][trkseg_0_trckpoint_0_lon][trkseg_0_trckpoint_0_ele],
                                    ...
                                    [trkseg_0_trckpoint_n_lat][trkseg_0_trckpoint_n_lon][trkseg_0_trckpoint_n_ele],
                                ], 
                                ...
                                [   [trkseg_n_trckpoint_0_lat][trkseg_n_trckpoint_0_lon][trkseg_n_trckpoint_0_ele],  
                                    ...
                                    [trkseg_n_trckpoint_n_lat][trkseg_n_trckpoint_n_lon][trkseg_n_trckpoint_n_ele],  
                ],
            ]
    """
    trks = []
    i = 0
    
    # Find all Tracks
    for trk in input_gpx.etree.findall("{*}trk"):   # Loop over a list of all tracks
        # Append a list for each track
        trks.append([])
        
        # Append the name of the track and another list for all tracksegments of that track
        name = trk.find("{*}name").text
        trks[i].append(name)
        trks[i].append([])
        n = 0
        
        # Find all tracksegments of the track
        for trkseg in trk.findall("{*}trkseg"): # Loop over all tracksegments of the track
            # append another List with all Trackpoints of that tracksegment
            trks[i][1].append([])
            
            # Find all trackpoints of that tracksegment
            for trkpt in trkseg.findall("{*}trkpt"):
                lat = float(trkpt.get("lat"))
                lon = float(trkpt.get("lon"))
                
                # Append optional elevation if the child-element "ele" exists
                ele = ""
                if trkpt.find("{*}ele") is not None:
                    ele = float(trkpt.find("{*}ele").text)
                
                # Append latitude, longitude and elevation for a trackpoint
                trks[i][1][n].append([lat, lon, ele])
            n = n + 1
        i = i + 1
    return trks

def print_list_trks(input_gpx: gpx) -> None:
    """Prints a list with all tracks

    Args:
        input_gpx (gpx): Data from the GPX-File
    """
    
    print_color("  Track-ID  |  Name    ")
    print_color("------------|----------")
    
    # Creates List of all tracks with their corrosponding tracksegments and trackpoints
    trks = _get_trks(input_gpx)
    
    # Prints the tracks in a list
    for id, trk in enumerate(trks):
        print_color(f"  {id:4}      |  {trk[id]}")

def print_list_trksegs(trk_id: int, input_gpx: gpx) -> bool:
    """Prints a list with all trackssegments
    
    Args:
        input_gpx (gpx): Data from the GPX-File
        
    Returns:
        bool: True, if tracksegment exists / False, if tracksegment doesnt exist
    """

    # Creates List of all tracks with their corrosponding tracksegments and trackpoints
    trks = _get_trks(input_gpx)
    
    # Check if tracksegments exist
    if not (0 <= trk_id < len(trks)):
        print_error("Error 300: Track außerhalb des gültigen Bereichs")
        return False
    
    print_color(" Tracksegment-ID | Trackpoints   ")
    print_color("-----------------|---------------")
    
    # print tracksegments in list
    for id, trkseg in enumerate(trks[trk_id][1]):
        print_color(f"  {id:4}           |  {len(trkseg):5}        ")
    
    return True

def print_list_trkpts(trk_id: int, trkseg_id: int, input_gpx: gpx) -> None:
    """Prints a list of all trackpoints from a choosen track and tracksegment with their corresponding latitude, longitude, and optional elevation.

    Args:
        input_gpx (gpx): Data from the GPX file
    """
    
    # Creates List of all tracks with their corrosponding tracksegments and trackpoints
    trks = _get_trks(input_gpx)
    
    # Checks if tracksegment exists
    if not (0 <= trkseg_id < len(trks[trk_id][1])):
        print_error("Error 301: Tracksegment ausserhalb des gültigen Bereichs!")
        return False
    
    print_color("   ID   |  Latitude  |  Longitude  |  Elevation  ")
    print_color("--------|------------|-------------|-------------")

    # Print trackpoint information in list form
    for id, trkpt in enumerate(trks[trk_id][1][trkseg_id]):
        if trkpt[2] != "":
            print_color(f"  {id: 4}  | {trkpt[0]: 10.6f} | {trkpt[1]: 11.6f} |  {trkpt[2]: 9.3f}  " ) 
        else:                            
            print_color(f"  {id: 4}  | {trkpt[0]: 10.6f} | {trkpt[1]: 11.6f} |             ")
            
    return True

def get_count(input_gpx: gpx) -> int:
    """Returns the number of tracks in the file.

    Args:
        input_gpx (gpx): Data from the GPX file

    Returns:
        int: Number of trackpoints
    """
    
    # Creates List of all tracks with their corrosponding tracksegments and trackpoints
    trkpts = _get_trks(input_gpx)
    
    # Retruns the numer of Elements (tracks)
    return len(trkpts)

def edit(trk_id: int, trkseg_id: int, trkpt_id: int, lat: float, lon: float, ele: float, input_gpx: gpx) -> None:
    """Edits the latitude, longitude, and elevation of a given trackpoint.

    Args:
        trk_id (int): ID of the trackpoint to edit
        trkseg_id (int): ID of the tracksegment that contains the trackpoint
        trkpt_id (int): ID of the track that contains the tracksegment
        lat (float): New Latitude / None: no changes
        lon (float): New Longitude / None: no changes
        ele (float): New Elevation / None: no changes
        input_gpx (gpx): Data from the GPX file
    """    
    
    # Find the specific "trkpt" element
    trks = _get_trks(input_gpx)

    # Check if trackpoint id is given
    if trkpt_id is None:
        print_error("Error 305: Kein Trackpoint ausgewählt!")
        return
    
    # Check if given trackpoint id exists
    if not (0 <= trkpt_id < len(trks[trk_id][1][trkseg_id])):
        print_error("Error 304: Trackpoint nicht vorhanden!")
        return
    
    # Find the specific Trackpoint
    trk = input_gpx.etree.findall("{*}trk")[trk_id]
    trkseg = trk.findall("{*}trkseg")[trkseg_id]
    trkpt = trkseg.findall("{*}trkpt")[trkpt_id]
    
    # Edit the latitude and longitude using the attributes "lat" and "lon"
    if lat is not None:
        # Check if latitude is in its Limits
        if not (-90 <= lat <= 90):
            print_error("Error 302: Latitude außerhalb des erlaubten Bereichs!  -90 <= Latitude <= 90")
            return
        trkpt.set("lat", str(lat))
        
    if lon is not None:
        # Check if latitude is in its Limits
        if not (-180 <= lon <= 180):
            print_error("Error 303: Latitude außerhalb des erlaubten Bereichs! -180 <= Longitude <= 180")
            return
        trkpt.set("lon", str(lon))
    
    if ele is not None:
        try:
            # Edit the elevation using the child element "ele", if it exists
            trkpt.find("{*}ele").text = str(ele)
        except Exception:
            # Create the child element "ele"
            trkpt.append(lxml.etree.Element("ele"))
            trkpt.find("{*}ele").text = str(ele)