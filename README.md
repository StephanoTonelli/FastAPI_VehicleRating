# Vehicle Scoring API

A lightweight, high-performance Vehicle Scoring REST API built with FastAPI.
This project provides endpoints to score individual or batch vehicle data based on simple business rules.

> **Note:** The scoring logic implemented in this API is **fictitious** and is intended only for demonstrating the API structure and functionality.

---

## Project Structure

```
vehicle_scoring_api/
├── app/
│   ├── main.py        # FastAPI application setup and router inclusion
│   ├── schemas.py     # Pydantic models for API request and response validation
│   ├── crud.py         # Business logic for vehicle scoring
│   ├── dependencies.py # API key authentication and security logic
│   └── routers/
│       └── scoring.py  # API routes for scoring operations (single and batch)
├── app/data/
│   └── api_keys.csv    # CSV file containing client_name, api_key, expiration_date
├── requirements.txt    # Python dependencies list
└── Dockerfile           # Docker container configuration
```

---

## How to Run Locally (Uvicorn)

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Application**
   ```bash
   uvicorn app.main:app --reload
   ```
   - `--reload` enables hot-reloading during development.

3. **Access the API Documentation**
   - Open your browser and navigate to:
      http://127.0.0.1:8000/docs
   - Use the Swagger UI page to **test** all available endpoints easily by sending requests directly from the browser.
   - **Authorization:** Click on the "Authorize" button to input your `X-API-Key` before testing endpoints.

---

## How to Build and Run with Docker

1. **Build the Docker Image**
   ```bash
   docker build -t vehicle-scoring-api .
   ```

2. **Run the Docker Container**
   ```bash
   docker run -d -p 80:80 vehicle-scoring-api
   ```

3. **Access the API**
   - Navigate to:
      http://localhost/docs

   - Use the Swagger UI to interact with and test the API endpoints inside the container.

---

## System Overview

| Layer                  | Components                     | Purpose                             |
|------------------------|---------------------------------|-------------------------------------|
| **API Layer**          | `main.py`, `routers/scoring.py` | Exposes REST API endpoints          |
| **Schema Layer**       | `schemas.py`                    | Validates and structures data       |
| **Business Logic Layer** | `crud.py`                     | Implements the in-memory scoring rules |
| **Security Layer**     | `dependencies.py`, `data/api_keys.csv` | Manages API key authentication |
| **Infrastructure**     | `Dockerfile`, `.dockerignore`   | Prepares the app for containerized deployment |

---

## Notes

- Scoring rules are **hardcoded** for now in `crud.py` but the structure allows easy future upgrades to database-driven scoring.
- API Key authentication is managed via a **CSV file (`api_keys.csv`)**.
- OpenAPI documentation is automatically generated at `/docs` when you run the app.
- **Reminder:** Scoring calculations are **artificial and intended only for demo/testing purposes**.

---

## How to Call the API via Postman

1. **Set Up Your Request**
   - Method: `POST`
   - URL for single scoring:
      http://127.0.0.1:8000/score/single

2. **Set Headers**
   - Key: `Content-Type`, Value: `application/json`
   - Key: `X-API-Key`, Value: `<your-api-key-here>` (example: `abc123`)

3. **Set Body** (raw JSON)
   Example:
   ```json
   {
     "make": "Toyota",
     "model": "Camry",
     "year": 2020,
     "mileage": 50000,
     "engine_size": 2.5
   }
   ```

4. **Send the Request**
   - You should receive a JSON response with the vehicle's score.

**Important:** Make sure your `api_keys.csv` contains the API key you are using and that the expiration date has not passed.

---

**Enjoy building and deploying your Vehicle Scoring API! 🚗📈**

