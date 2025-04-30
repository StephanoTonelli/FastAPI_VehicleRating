Great curiosity — and a smart one! If you want to move from **local file storage** (CSV + SQLite) to a **real database in Azure**, here's what you need to do, step-by-step:

---

## ✅ Goal

- Store your `api_keys.csv` and `scoring_variables.csv` as real **database tables**
- Replace `logs.db` with a **persistent cloud SQL database**
- Fully integrate with **Azure SQL Database** (or an alternative like PostgreSQL on Azure)

---

## 🔧 Step-by-Step Migration Plan

### 🟦 1. Choose Your Azure Database

Azure supports several managed SQL options. Two great fits:

| Option             | Why Use It?                      |
|--------------------|----------------------------------|
| **Azure SQL Database** | Scalable, Microsoft-native, full T-SQL |
| **Azure Database for PostgreSQL** | Very flexible, great with SQLAlchemy |

💡 Let's assume you use **Azure SQL** or **PostgreSQL**.

---

### 🗃️ 2. Migrate Your CSVs to SQL Tables

#### `api_keys.csv` → `api_keys` table

```sql
CREATE TABLE api_keys (
    client_name VARCHAR(100),
    api_key VARCHAR(100) PRIMARY KEY,
    expiration_date DATE
);
```

#### `scoring_variables.csv` → `scoring_variables` table

```sql
CREATE TABLE scoring_variables (
    variable VARCHAR(100),
    Toyota_Camry FLOAT,
    Honda_Civic FLOAT,
    Ford_F150 FLOAT
);
```

✅ Use a GUI like:
- Azure Data Studio
- pgAdmin (for PostgreSQL)
- DBeaver
- or a migration script with `pandas.to_sql()`

---

### 🧠 3. Replace `pandas.read_csv()` with SQL queries

#### Old (CSV):
```python
df = pd.read_csv("app/data/scoring_variables.csv")
```

#### New (SQL):
```python
import sqlalchemy

engine = sqlalchemy.create_engine(AZURE_DB_CONNECTION_STRING)
df = pd.read_sql("SELECT * FROM scoring_variables", con=engine)
```

---

### 📋 4. Replace SQLite with Azure SQL/PostgreSQL for logs

- Modify `DATABASE_URL` in your `database.py`:
```python
DATABASE_URL = "postgresql://username:password@host:port/database"
```

OR for Azure SQL:
```python
DATABASE_URL = "mssql+pyodbc://username:password@yourserver.database.windows.net/dbname?driver=ODBC+Driver+17+for+SQL+Server"
```

- Run `Base.metadata.create_all(bind=engine)` as usual — it will now create your `request_logs` table in the cloud DB.

---

### 🔐 5. Handle Secrets Securely

Use **Azure Key Vault** or `.env` files for storing:

- DB connection string
- API secrets

Never hardcode them in code.

---

### 🚀 6. Deploy Your FastAPI App (Optional)

- Use **Azure App Service**, **Azure Container Apps**, or **Azure Kubernetes Service (AKS)** to host your FastAPI app
- Connect it to your Azure-hosted database

---

## ✅ Benefits of Moving to Azure SQL/PostgreSQL

| Feature | Benefit |
|--------|---------|
| Cloud persistence | No data loss on container shutdown |
| Multi-container support | App can scale freely |
| Better analytics | Run queries on scoring and usage history |
| Centralized auth control | Manage API clients securely |

---

## 🔄 Summary

| What | Replace with |
|------|--------------|
| `api_keys.csv` | Azure SQL table (`api_keys`) |
| `scoring_variables.csv` | Azure SQL table (`scoring_variables`) |
| `logs.db` (SQLite) | Azure SQL/PostgreSQL (`request_logs`) |
| Local `read_csv` | `pd.read_sql()` |
| Local DB URL | Azure DB URL in `DATABASE_URL` |

---




# 🚀 Guide to Deploy Your FastAPI Vehicle Scoring API on Azure with Azure SQL

This guide assumes:
- You are containerizing your FastAPI app using Docker
- You're deploying it to Azure (App Service or Container App)
- You want to use **Azure SQL Database** instead of local SQLite and CSV files

---

## ✅ Step 1: Set Up Azure SQL Database

1. Go to [Azure Portal](https://portal.azure.com/)
2. Create a **SQL Database** (single or serverless is fine)
3. Set the following:
   - Choose or create a **SQL Server**
   - Allow Azure services and your IP in the firewall rules
4. After creation:
   - Copy the **connection string** (ADO.NET format is best)
   - Example:
     ```
     Server=tcp:yourserver.database.windows.net,1433;Database=vehicle_scoring;User ID=youruser;Password=yourpassword;Encrypt=true;Connection Timeout=30;
     ```

---

## ✅ Step 2: Create SQL Tables

Use **Azure Data Studio** or `sqlcmd` to create the tables below.

### `api_keys` Table
```sql
CREATE TABLE api_keys (
    api_key VARCHAR(255) PRIMARY KEY,
    client_name VARCHAR(255) NOT NULL,
    expiration_date DATE NOT NULL
);
```

### `scoring_variables` Table
```sql
CREATE TABLE scoring_variables (
    variable VARCHAR(255) PRIMARY KEY,
    Toyota_Camry FLOAT,
    Honda_Civic FLOAT,
    Ford_F150 FLOAT
);
```

### `request_logs` Table
```sql
CREATE TABLE request_logs (
    id INT IDENTITY(1,1) PRIMARY KEY,
    timestamp DATETIME,
    headers NVARCHAR(MAX),
    path NVARCHAR(255),
    method NVARCHAR(10),
    status_code INT,
    response_body NVARCHAR(MAX),
    client_name NVARCHAR(255)
);
```

---

## ✅ Step 3: Update Your FastAPI Code

### 🔄 `database.py`
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
```

### 🗝️ `.env`
Create a file named `.env`:
```env
DATABASE_URL=mssql+pyodbc://youruser:yourpassword@yourserver.database.windows.net:1433/vehicle_scoring?driver=ODBC+Driver+17+for+SQL+Server
```

---

## ✅ Step 4: Replace CSV File Loaders with SQL Queries

### 🔁 `authentication.py`
Replace CSV loading with a SQL query:
```python
import pandas as pd
from sqlalchemy import text
from .database import engine

with engine.connect() as conn:
    df = pd.read_sql("SELECT * FROM api_keys", conn)
    # Convert df to API_KEYS dictionary
```

### 🔁 `scoring_logic.py`
```python
scoring_variables_df = pd.read_sql("SELECT * FROM scoring_variables", engine)
```

---

## ✅ Step 5: Update Dockerfile
Ensure ODBC drivers are installed for SQL Server.

### 🔧 Updated Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install ODBC driver and dependencies
RUN apt-get update && \
    apt-get install -y gcc g++ gnupg unixodbc-dev curl && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

---

## ✅ Step 6: Build and Push Docker Image

1. **Build your Docker image locally**:
   ```bash
   docker build -t yourdockerhubusername/vehicle-scoring-api:latest .
   ```

2. **Login to Docker Hub**:
   ```bash
   docker login
   ```

3. **Push image to Docker Hub**:
   ```bash
   docker push yourdockerhubusername/vehicle-scoring-api:latest
   ```

---

## ✅ Step 7: Deploy to Azure App Service (with Docker Container)

1. Go to Azure Portal
2. Create a new **App Service**
3. Select:
   - **Docker container**
   - **Linux OS**
4. Under **Container settings**:
   - Image source: **Docker Hub**
   - Image: `yourdockerhubusername/vehicle-scoring-api`
5. Under **Configuration > Application settings**, add:
   - `DATABASE_URL` (use the same value from your `.env` file)
6. Save and restart the App Service

---

## ✅ Step 8: Test Your Deployment

1. Navigate to:
   ```
   https://<your-app-name>.azurewebsites.net/docs
   ```
2. Use Swagger UI to test the `/score/single` endpoint
3. Verify that logs are saved in your Azure SQL database

---

## 🎯 You're Live in Azure!

You’ve:
- Replaced local files with Azure SQL
- Containerized your app
- Deployed to Azure with a persistent backend

Let me know if you'd like a full sample `docker-compose` + `.env` + SQLAlchemy schema template!

