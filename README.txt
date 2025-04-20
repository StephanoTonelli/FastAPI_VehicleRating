vehicle_scoring_api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers/
│       └── scoring.py
├── data/
├── requirements.txt
└── Dockerfile

To run uvicorn:
    uvicorn app.main:app --reload

To access the API documentation:
    http://127.0.0.1:8000/docs