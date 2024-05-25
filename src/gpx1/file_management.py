from tkinter import *
from tkinter import filedialog

def openFile():                                                 
    filepath = filedialog.askopenfilename()                                 # zuweisung des file-pfades der filepath variable
    if filepath:                                                            # -> wenn eine Datei ausgewählt wird
        try:
            with open(filepath, 'r') as file:                               # zuweisung von des file-pfades(filepath) der open funktion
                content = file.read()                                       # lesen des zugewiesenen files
                print(content)                                              # nur zu Test-zwecken Ausgabe des File Inhaltes auf der Konsole
                window.destroy()                                            # schließen des "Öffnen-Knopf" Fensters nach benutzung
                return content
        except Exception as e:
            print(f"Fehler beim Laden der Datei: {e}")                      # prüfen auf Fehler beim datei laden
    else:                                                                   # -> wenn keine Datei asugewählt wird
        print("Keine Datei ausgewählt.")                                    
        window.destroy()

window = Tk()                                                               # Fenster für "Öffnen-Knopf"
button = Button(window, text="Öffnen", command=openFile)
button.pack()
window.mainloop()
