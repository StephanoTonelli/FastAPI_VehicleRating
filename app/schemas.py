from pydantic import BaseModel
from typing import List, Optional

class VehicleData(BaseModel):
    make: str
    model: str
    year: int
    mileage: Optional[float] = None
    engine_size: Optional[float] = None
    # … add any other raw vehicle fields here …

class VehicleScore(VehicleData):
    score: float

class BatchRequest(BaseModel):
    vehicles: List[VehicleData]

class BatchResponse(BaseModel):
    results: List[VehicleScore]
