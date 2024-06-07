""" __init__.py

Beschreibung: Editor, mit dem GPX-Dateien bearbeitet werden können
Autor: Pascal Köhnlein
Erstellt: 19.05.2024
"""

from . import parser
from . import routs
from . import track
from . import file_management
from gpx1.usefull import input_type, PrintColor



def Main():

    #Deklarieren von Laufvariablen
    Startabfrage = 0
    Funktionauswahl = 0
    Modulabfrage = 0

    #Start des Programmes
    PrintColor("Willkommen im GPX-Editor")
    PrintColor("Bitte wählen Sie aus folgenden Optionen aus:")

    #Eingangs abfrage: Auswahl einer Datei
    while True:
        PrintColor("0: Programm Beenden ")
        PrintColor("1: Auswahl einer GPX Datei")
        Startabfrage = input()

    #Soll Programm beendet werden?
        if Startabfrage == "0" or Startabfrage == "1":
            break
            
        else:
            PrintColor("Wählen sie bitte nur zwischen 0 & 1")

        #Auswahl einer Datei treffen
    while Startabfrage == "1": 
        PrintColor("Wählen Sie bitte die gewünschte Datei aus")
        input_gpx = file_management.open_file()

        PrintColor(f"Anzahl Waypoints: {waypoints.get_count(input_gpx)}")
        PrintColor(f"Anzahl Tracks: {track.get_count(input_gpx)}")
        PrintColor(f"Anzahl Routs: {routs.get_count(input_gpx)}")

        #Auswahl zwischen den Funktionen
        while True:
            PrintColor("Wählen sie bitte zwischen folgenden Optionen aus:")
            PrintColor("0: Programm beenden")
            PrintColor("1: Waypoints")
            PrintColor("2: Tracks")
            PrintColor("3: Routs")
            PrintColor("4: Metadaten")
            Modulabfrage = input()


            #Beenden des Programms
            if Modulabfrage == "0":
                Startabfrage = "0"
                break
        
                
            elif Modulabfrage == "1":

                while True:
                    
                    PrintColor("1. Bearbeiten von Waypoints")
                    PrintColor("2. Höhendifferenz zw. zwei Waypoints berechnen")
                    PrintColor("0. Hauptmenü")
                    Funktionauswahl = input()

                    if Funktionauswahl == "1":
                        PrintColor("Geben sie bitte folgende Daten an")
                        PrintColor("Bitte beachten sie den geforderten Datentyp in der Klammer")
                        PrintColor("ID:(Integer)")
                        id = input()
                        PrintColor("Latitute:(Float)")
                        lat = input()
                        PrintColor("longitut:(Float)")
                        lon = input()
                        PrintColor("Elevation:(Float)")
                        ele = input()
                        waypoints.edit(id, lat, lon, ele, input_gpx)
                    
                    elif Funktionauswahl == "2"
                        PrintColor("Geben sie die IDs der Wegpunkte an")
                        PrintColor("ID 1:(Integer)")
                        id1 = input()
                        PrintColor("ID 2:(Integer)")
                        id2 = input()
                        waypoints.calc_elevation(id1, id2, input_gpx)


                    elif Funktionauswahl == "0"
                        break

                    else:
                        PrintColor("Unzulässige Eingabe")
                
            elif Modulabfrage == "2":


                while True:
                    PrintColor("1. Bearbeiten eines Trackpoints")
                    PrintColor("0. Hauptmenü")
                    Funktionauswahl = input()

                    if Funktionauswahl == "1":
                        track.edit(input_gpx)

                    elif Funktionauswahl == "0"
                        break

                    else:
                        PrintColor("Unzulässige Eingabe")

                
            elif Modulabfrage == "3":
                

                while True:
                    PrintColor("1. Bearbeiten eines Routpoints")
                    PrintColor("2. Startpunkt festlegen")
                    PrintColor("0. Hauptmenü")
                    Funktionauswahl = input()
                    if Funktionauswahl == "1":
                        routs.edit(input_gpx)
                    
                    elif Funktionauswahl == "2"
                        routs.edit_startpoint(input_gpx)

                    elif Funktionauswahl == "0"
                        break

                    else:
                        PrintColor("Unzulässige Eingabe")
                
            elif Modulabfrage == "4":
                PrintColor("Name:")
                PrintColor("Beschreibung")
                PrintColor("Autor")

                while True:
                PrintColor("1. Bearbeiten der Metadaten")
                PrintColor("0. Hauptmenü")
                Funktionauswahl = input()
                    if Funktionauswahl == "1":
                        #Funktion einfügen

                    elif Funktionauswahl == "0"
                        break

                    else:
                        PrintColor("Unzulässige Eingabe")

        #Programm wird beendet
        if Startabfrage == "0":
        
            break