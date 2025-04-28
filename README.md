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
│   ├── database.py    # (currently unused) Database configuration for future expansion
│   ├── models.py      # (currently unused) Database models for Vehicle and ScoreRule
│   ├── schemas.py     # Pydantic models for API request and response validation
│   ├── crud.py         # Business logic for vehicle scoring
│   └── routers/
│       └── scoring.py  # API routes for scoring operations (single and batch)
├── data/               # Folder reserved for any data files (optional)
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
   - You can use this Swagger UI page to **test** all available endpoints easily by sending requests directly from the browser.

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
| **Infrastructure**     | `Dockerfile`, `.dockerignore`   | Prepares the app for containerized deployment |

---

## Notes

- The database layer (`database.py`, `models.py`) is defined but **currently not active**.
- Scoring rules are **hardcoded** for now in `crud.py` but the structure allows easy future upgrades to database-driven scoring.
- OpenAPI documentation is automatically generated at `/docs` when you run the app.
- **Reminder:** Scoring calculations are **artificial and intended only for demo/testing purposes**.

---

## Future Improvements (Optional)
- Make scoring rules dynamic by reading from a database.
- Add authentication and authorization for the scoring API.
- Create a frontend dashboard to upload vehicle data and visualize scores.

---

**Enjoy building and deploying your Vehicle Scoring API! 🚗📈**

