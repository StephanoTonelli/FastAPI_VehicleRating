from fastapi import FastAPI  # Importing FastAPI class to create the web application
import uvicorn  # Importing Uvicorn server to run the FastAPI application
from .routers.scoring import router as scoring_router  # Importing the 'router' from the 'scoring' module inside the 'routers' package and aliasing it as 'scoring_router'

app = FastAPI(title="Vehicle Scoring API")  # Initializing the FastAPI application with the title "Vehicle Scoring API"

app.include_router(scoring_router)  # Including the scoring_router into the FastAPI app to handle routes defined in the 'scoring' module

if __name__ == "__main__":  # Checking if this script is the main program being run (not imported as a module)
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)  # Running the app with uvicorn, binding to all IP addresses (0.0.0.0) on port 80, and enabling auto-reload on code changes

@app.get("/", summary="Health check")  # Defining a GET endpoint at the root URL "/" with a summary description "Health check"
def health_check():  # Defining the handler function for the root endpoint
    return {"status": "ok"}  # Returning a simple JSON response to indicate that the API is alive and healthy
