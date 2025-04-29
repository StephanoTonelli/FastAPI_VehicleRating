import os  # Import os module to work with file paths
import pandas as pd  # Import pandas to read CSV easily
from datetime import datetime, timezone  # Import datetime to handle expiration dates
from fastapi import Header, HTTPException  # Import FastAPI tools to extract headers and raise errors
from typing import Dict  # Import Dict type for type hinting


# Base directory where your project root is
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Full path to app/data/api_keys.csv
API_KEYS_FILE = os.path.join(BASE_DIR, "app", "data", "api_keys.csv")

def load_api_keys() -> Dict[str, datetime]:
    """
    Load API keys and their expiration dates from the CSV file into a dictionary.
    Returns a dict where key is API key string and value is expiration date (datetime object).
    """
    api_keys = {}  # Initialize an empty dictionary to store API keys and expiration dates
    try: # Check if the file exists before trying to open it
        df = pd.read_csv(API_KEYS_FILE)  # Read the CSV into a pandas DataFrame
        print(f"Loaded DataFrame:\n{df}")  # Debug print to check contents
        for _, row in df.iterrows():  # Iterate over each row in the DataFrame
            print(f"Row read from CSV: {row}")  # <-- Add this print statement for debugging
            key = str(row["api_key"]).strip()  # Extract and strip the API key # <-- .strip() removes leading/trailing spaces
            expiration = datetime.strptime(str(row["expiration_date"]).strip(), "%Y-%m-%d").replace(tzinfo=timezone.utc)  # Parse expiration date string into datetime object
            api_keys[key] = expiration  # Store the API key and its expiration date in the dictionary
    except FileNotFoundError:
        print(f"ERROR: Could not find file {API_KEYS_FILE}")
    except Exception as e:
        print(f"ERROR while loading API keys: {e}")

    print(f"Loaded API keys: {api_keys}")  # Debug print statement to show loaded API keys
    # Note: In production, consider using logging instead of print for better log management
    return api_keys  # Return the populated dictionary

# Preload API keys into memory at startup
API_KEYS = load_api_keys()  # Load API keys once when the server starts

def verify_api_key(x_api_key: str = Header(...)):
    """
    Dependency function to verify the provided API key.
    """
    print(f"Received API key from client: {x_api_key}")  # <-- Print received key for debugging
    if x_api_key not in API_KEYS:  # Check if the provided API key exists in the loaded API keys
        raise HTTPException(status_code=401, detail="Invalid API Key")  # Raise error if API key is invalid

    expiration_date = API_KEYS[x_api_key]  # Retrieve the expiration date for the provided API key
    if datetime.now(timezone.utc) > expiration_date:  # Compare current UTC time with expiration date
        raise HTTPException(status_code=401, detail="API Key Expired")  # Raise error if the API key has expired

