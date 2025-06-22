# etl/extract.py
import pandas as pd

def extract_from_json(file_path: str) -> pd.DataFrame:
    """Extracts data from a JSON file."""
    print(f"Extracting data from {file_path}...")
    # --- THIS IS THE CORRECTED LINE ---
    return pd.read_json(file_path, dtype=False) 

def extract_from_csv(file_path: str) -> pd.DataFrame:
    """Extracts data from a CSV file."""
    print(f"Extracting data from {file_path}...")
    return pd.read_csv(file_path)