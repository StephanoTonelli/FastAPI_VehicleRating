from fastapi import FastAPI
from .routers.scoring import router as scoring_router

app = FastAPI(title="Vehicle Scoring API")
app.include_router(scoring_router)

@app.get("/", summary="Health check")
def health_check():
    return {"status": "ok"}
