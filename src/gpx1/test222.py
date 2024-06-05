# C:\Users\user\Desktop\GPX1-main\src\gpx1\test_import.py
try:
    from gpx1 import track_module
    print("Module imported successfully.")
except ImportError as e:
    print(f"Error importing module: {e}")
