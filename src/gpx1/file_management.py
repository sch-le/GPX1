""" file_management.py

Beschreibung: Erstellen eines Fensters zum auswählen und verwenden von GPX-Dateien unter verwendung von parser.py
Autor: Lukas Reißmann
Erstellt: 06.06.2024
"""
from tkinter import *
from tkinter import filedialog
import os

#Importieren der notwendigen Funktionen aus parser.py
from gpx1.parser import parse, write_file

def open_file():                                                 
    filepath = filedialog.askopenfilename(
        #Beschränken der Auswahl auf GPX-Dateien
        filetypes=[("GPX files", "*.gpx")]  
    )
    
    if filepath:                                                            
        if not filepath.endswith('.gpx'):
            print("Fehler: Bitte wählen Sie eine GPX-Datei aus.")
        else:
            try:
                #Verwenden der parse-Funktion aus parser.py
                gpx_data = parse(filepath)  
                if gpx_data:
                    print("GPX-Datei erfolgreich geparst:")               
                    write_file(gpx_data)  #GPX-Datei schreiben
                else:
                    print("Fehler beim Parsen der GPX-Datei.")
            except Exception as e:
                print(f"Fehler beim Laden der Datei: {e}")
    else:                                                                   
        print("Keine Datei ausgewählt.")                                    

    window.destroy()

#Erstellen des Hauptfensters
window = Tk()                                                               
window.title("GPX Datei Öffnen")

#Erstellen und platzieren des "Öffnen" Buttons
button = Button(window, text="Öffnen", command=open_file)
button.pack(pady=20)

#Starten der Tkinter-Ereignisschleife
window.mainloop()
