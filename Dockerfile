# 1) Pick a small Python base
FROM python:3.12-0

# 2) Set your working directory
WORKDIR /app

# 3) Install system deps (if any)
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc \
 && rm -rf /var/lib/apt/lists/*

# 4) Copy & install Python deps
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# 5) Copy your code
COPY . .

# 6) Expose and run
EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
