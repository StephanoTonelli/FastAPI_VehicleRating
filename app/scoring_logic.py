import pandas as pd  # Import pandas to load the CSV
import os  # To manage file paths
from fastapi import HTTPException  # To raise errors if make/model is missing
from datetime import datetime
from .schemas import VehicleData

# Base project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the scoring variables CSV
SCORING_VARIABLES_FILE = os.path.join(BASE_DIR, "app", "data", "scoring_variables.csv")

# Load the scoring variables CSV into a DataFrame
try:
    scoring_variables_df = pd.read_csv(SCORING_VARIABLES_FILE)
    
    #print(f"Scoring Variables Loaded:\n{scoring_variables_df}")  # DEBUG PRINT

except Exception as e:
    print(f"Error loading scoring variables: {e}")
    scoring_variables_df = None  # In case of loading error

def calculate_score_from_data(v: VehicleData) -> float:
    """
    Calculate the score for a vehicle based on dynamic scoring variables loaded from CSV.
    """
    if scoring_variables_df is None:
        raise HTTPException(status_code=500, detail="Scoring variables not loaded.")

    make_model_key = f"{v.make}_{v.model}".replace(" ", "_")  # Normalize Make_Model key (spaces replaced by _)

    if make_model_key not in scoring_variables_df.columns:
        raise HTTPException(
            status_code=422,
            detail=f"Scoring rules not found for make/model: {make_model_key}"
        )

    # Extract the scoring variables for the given make/model
    variables = scoring_variables_df.set_index("variable")[make_model_key]
    print(f"scoring variables: {variables}") # Debug print to check loaded variables


    total_score = 0.0  # Initialize total score

    # Apply scoring rules
    age = datetime.utcnow().year - v.year
    age_weight = float(variables["age_weight"])  # Get age_weight from variables
    total_score += max(0, age) * age_weight  # Score based on vehicle's age

    if v.mileage is not None:
        mileage_bonus = float(variables["mileage_bonus"])  # Get mileage_bonus
        total_score += (100_000 - v.mileage) * mileage_bonus  # Reward lower mileage

    if v.engine_size is not None:
        engine_size_bonus = float(variables["engine_size_bonus"])  # Get engine_size_bonus
        total_score += v.engine_size * engine_size_bonus  # Score based on engine size

    return round(total_score, 2)  # Return rounded total score
