from .schemas import VehicleData

def calculate_score_from_data(v: VehicleData) -> float:
    # pull your scoring rules from DB or in‑memory…
    # for example:
    total = 0.0
    age = 2025 - v.year
    total += max(0, age) * 1.5   # pretend “age” rule
    if v.mileage:
        total += (100_000 - v.mileage) * 0.01
    # … more rule applications …
    return round(total, 2)
