from fastapi import FastAPI, Request, Response # Importing FastAPI class to create the web application
import uvicorn  # Importing Uvicorn server to run the FastAPI application
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
import json

from .routers.scoring import router as scoring_router  # Import your API router
from .authentication import verify_api_key, API_KEYS  # Optional: if using Depends for authentication
from .database import engine, SessionLocal  # SQLAlchemy engine and session
from .models_log import Base, RequestLog  # Your request log table model


# ----------------------------------------------------------
# Initialize FastAPI app
# ----------------------------------------------------------
app = FastAPI(title="Vehicle Scoring API")  # Initializing the FastAPI application with the title "Vehicle Scoring API"

# ----------------------------------------------------------
# CORS Middleware (optional, useful if you test from browser)
# ----------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------
# Middleware: Custom logging middleware to record all requests
# ----------------------------------------------------------
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        headers = dict(request.headers)  # Capture request headers
        path = request.url.path
        method = request.method
        
        # Extract API key and look up client name
        api_key = headers.get("x-api-key")
        client_name = None
        if api_key in API_KEYS:
            client_name = API_KEYS[api_key]["client_name"]

        response = await call_next(request)  # Call the actual route handler

        try:
            # Read the response body (needed for logging)
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
                # Rebuild body_iterator as an async generator
                async def new_body_iterator():
                    yield body

            response.body_iterator = new_body_iterator()  # ✅ fix here
            response_text = body.decode("utf-8")

            # Save request log to DB
            db = SessionLocal()
            log_entry = RequestLog(
                timestamp=datetime.utcnow(),
                headers=json.dumps(headers),
                path=path,
                method=method,
                status_code=response.status_code,
                response_body=response_text,#[:10000],  # Truncate to avoid large entries
                client_name=client_name  # store client name in DB
            )
            db.add(log_entry)
            db.commit()
            db.close()

        except Exception as e:
            print(f"Logging failed: {e}")

        return response

app.add_middleware(LoggingMiddleware)  # Register the middleware

# ----------------------------------------------------------
# Startup event: Create tables (like request_logs) at startup
# ----------------------------------------------------------
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)  # Ensure all tables are created


# ----------------------------------------------------------
# Include routers (API endpoints)
# ----------------------------------------------------------
app.include_router(scoring_router) # Including the scoring_router into the FastAPI app to handle routes defined in the 'scoring' module



# ----------------------------------------------------------
# useful for running the app as "python -m app.main"
# ----------------------------------------------------------
if __name__ == "__main__":  # Checking if this script is the main program being run (not imported as a module)
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)  # Running the app with uvicorn, binding to all IP addresses (0.0.0.0) on port 80, and enabling auto-reload on code changes


# ----------------------------------------------------------
# Health check endpoint (optional but useful)
# ----------------------------------------------------------
@app.get("/", summary="Health check")  # Defining a GET endpoint at the root URL "/" with a summary description "Health check"
def health_check():  # Defining the handler function for the root endpoint
    return {"status": "ok"}  # Returning a simple JSON response to indicate that the API is alive and healthy
