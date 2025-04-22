from fastapi import FastAPI
import uvicorn
from .routers.scoring import router as scoring_router

app = FastAPI(title="Vehicle Scoring API")
app.include_router(scoring_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)

@app.get("/", summary="Health check")
def health_check():
    return {"status": "ok"}
