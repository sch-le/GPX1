""" file_management.py

Beschreibung: Erstellen eines Fensters zum auswählen und verwenden von GPX-Dateien unter verwendung von parser.py
Autor: Lukas Reißmann
Erstellt: 06.06.2024
"""

from tkinter import filedialog

#Importieren der notwendigen Funktionen aus parser.py
from gpx1.parser import parse
from gpx1.usefull import print_color

def open_file():
    #while True:                                              
    filepath = filedialog.askopenfilename(
        title="GPX-Datei auswählen",
        #Beschränken der Auswahl auf GPX-Dateien
        filetypes=[("GPX files", "*.gpx")]  
    )
    
    if filepath:                                                            
        if not filepath.endswith('.gpx'):
            print_color("Fehler: Bitte wählen Sie eine GPX-Datei aus.")
        else:
            try:
                #Verwenden der parse-Funktion aus parser.py
                gpx_data = parse(filepath)  
                return gpx_data
            
            except Exception as e:
                print_color(f"Fehler beim Laden der Datei: {e}")
    else:                                                                   
        print_color("Keine Datei ausgewählt.")  


def save_path():
    filepath = filedialog.asksaveasfilename(
        title="Speicherort auswählen",
        defaultextension=".gpx",
        filetypes=[("GPX files", "*.gpx")]
    )   
    if filepath:
        return filepath
    else:
        print_color("Kein Speicherort ausgewählt.")
        return None
