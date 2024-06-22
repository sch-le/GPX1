""" config.py

(c) PaFeLe²KyLuKa-Industries

Beschreibung: verschiedene Konfigurationen
Autor: Leon Schuck
Erstellt: 27.05.2024
"""

# Version
version = "V1.0"

# Pfad und Name mit dem die Datei auf Mac ausgegeben wird
output_path = "output.gpx"

class gpx:
    """Klasse zum Speichern von GPX-Daten und XML-Deklaration
    """
    # XML-Deklarationen
    encoding = None
    standalone = None

    # GPX-Daten
    etree = None