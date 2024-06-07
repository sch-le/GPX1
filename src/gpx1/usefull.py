#Einführen von Colorama
from colorama import init, Fore, Back, Style

def input_type(type: str):
    
    
    while True:

        input_str = input()

        if input_str is None:
            return

        if type == int:
            try:
                return int(input_str, 10) 
            except Exception:
                PrintColor("Falscher Datentyp")
                continue         
        
        elif type == float:
            try:
                return float(input_str, 10)    
            except Exception:
                PrintColor("Falscher Datentyp")
                continue

#Globale Variablen
count = 0

#Funktionen
#Erstellen der Farbwechsel Funktion
def PrintColor (Text):
    #Hier wird mit Globalen Variablen gearbeitet
    global count
    #Ist count gerade dann wird ein schwarzer Hintergrund ausgegeben
    if count % 2 == 0 :
        print (Fore.YELLOW + Back.BLACK + Text + Style.RESET_ALL)

    #Ist count ungerade dann wird ein roter Hintergrund ausgegeben
    elif count % 2 == 1:
        print(Fore.YELLOW + Back.RED + Text + Style.RESET_ALL)
    count = count + 1