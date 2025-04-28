from .schemas import VehicleData  # Importing VehicleData schema to type the input parameter

def calculate_score_from_data(v: VehicleData) -> float:  # Defining a function that calculates a score based on a VehicleData object
    # pull your scoring rules from DB or in‑memory…  # Placeholder comment suggesting that rules could be pulled from DB later
    # for example:

    total = 0.0  # Initializing the total score to 0.0

    age = 2025 - v.year  # Calculating the vehicle's age based on the year 2025 (assumed current year)
    total += max(0, age) * 1.5  # Adding 1.5 points for every year of age, but not allowing negative ages

    if v.mileage:  # Checking if mileage data is provided (mileage could be None)
        total += (100_000 - v.mileage) * 0.01  # Rewarding lower mileage: vehicles closer to 0 miles get higher scores

    # … more rule applications …  # Placeholder to add additional scoring logic (e.g., based on engine size, fuel type)

    return round(total, 2)  # Rounding the total score to 2 decimal places before returning
