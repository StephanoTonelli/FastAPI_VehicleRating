from fastapi import APIRouter, HTTPException  # Importing APIRouter to create route groups, HTTPException for handling errors
from typing import List  # Importing List type for type annotations
from .. import schemas, scoring_logic  # Importing the 'crud' module for business logic and 'schemas' for data validation and structure
from fastapi import Depends
from ..authentication import verify_api_key

router = APIRouter(
    prefix="/score",
    tags=["scoring"],
    dependencies=[Depends(verify_api_key)]  # <-- Require API Key for ALL routes in this router
) # Initializing an API router with a URL prefix "/score" and tagging it as "scoring"


@router.post(
    "/single",
    response_model=schemas.VehicleScore,
    summary="Score a single vehicle"
)  # Defining a POST endpoint at "/score/single", returning a VehicleScore schema, and summarizing the purpose
def score_single(vehicle: schemas.VehicleData):  # Defining the handler function that takes a VehicleData object as input
    score = scoring_logic.calculate_score_from_data(vehicle)  # Calling the business logic function to calculate the score for the input vehicle
    return schemas.VehicleScore(**vehicle.dict(), score=score)  # Returning a VehicleScore object by merging the input vehicle data with the calculated score


"""
@router.post(
    "/batch",
    response_model=schemas.BatchResponse,
    summary="Score a batch of vehicles"
)  # Defining a POST endpoint at "/score/batch", returning a BatchResponse schema, and summarizing the purpose
def score_batch(req: schemas.BatchRequest):  # Defining the handler function that takes a BatchRequest object containing multiple vehicles
    results: List[schemas.VehicleScore] = []  # Initializing an empty list to store the scored vehicles
    for v in req.vehicles:  # Looping through each vehicle in the incoming batch request
        sc = scoring_logic.calculate_score_from_data(v)  # Calculating the score for each individual vehicle
        results.append(schemas.VehicleScore(**v.dict(), score=sc))  # Appending a new VehicleScore object to the results list
    return schemas.BatchResponse(results=results)  # Returning the batch of scored vehicles encapsulated inside a BatchResponse
"""