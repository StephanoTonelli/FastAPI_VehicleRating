from fastapi import APIRouter, HTTPException
from typing import List
from .. import crud, schemas

router = APIRouter(prefix="/score", tags=["scoring"])

@router.post(
    "/single",
    response_model=schemas.VehicleScore,
    summary="Score a single vehicle"
)
def score_single(vehicle: schemas.VehicleData):
    score = crud.calculate_score_from_data(vehicle)
    return schemas.VehicleScore(**vehicle.dict(), score=score)

@router.post(
    "/batch",
    response_model=schemas.BatchResponse,
    summary="Score a batch of vehicles"
)
def score_batch(req: schemas.BatchRequest):
    results: List[schemas.VehicleScore] = []
    for v in req.vehicles:
        sc = crud.calculate_score_from_data(v)
        results.append(schemas.VehicleScore(**v.dict(), score=sc))
    return schemas.BatchResponse(results=results)
