from pydantic import BaseModel  # Importing BaseModel from Pydantic to define data models with validation
from typing import List, Optional  # Importing List and Optional types for type annotations

class VehicleData(BaseModel):  # Defining a Pydantic model to represent raw vehicle input data
    make: str  # The make (manufacturer) of the vehicle (e.g., "Toyota"), required field
    model: str  # The model of the vehicle (e.g., "Camry"), required field
    year: int  # The production year of the vehicle, required field
    mileage: Optional[float] = None  # Optional mileage of the vehicle (may be None if not provided)
    engine_size: Optional[float] = None  # Optional engine size of the vehicle (may be None if not provided)
    # … add any other raw vehicle fields here …  # Placeholder for extending the schema with additional attributes

class VehicleScore(VehicleData):  # Defining a model that extends VehicleData by adding a score field
    score: float  # The computed score for the vehicle based on its attributes

class BatchRequest(BaseModel):  # Defining a model for the incoming batch scoring request
    vehicles: List[VehicleData]  # A list of vehicles to be scored

class BatchResponse(BaseModel):  # Defining a model for the batch scoring response
    results: List[VehicleScore]  # A list of scored vehicles returned in the response
